#!/bin/bash
# K3s 自动化部署脚本
# 用法：./deploy-k3s.sh --master <ip> --masters-user <user> --masters-pass <pass> --worker <ip1,ip2> --workers-user <user> --workers-pass <pass>

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --master) MASTER_IP="$2"; shift 2 ;;
        --masters-user) MASTER_USER="$2"; shift 2 ;;
        --masters-pass) MASTER_PASS="$2"; shift 2 ;;
        --worker) WORKER_IPS="$2"; shift 2 ;;
        --workers-user) WORKER_USER="$2"; shift 2 ;;
        --workers-pass) WORKER_PASS="$2"; shift 2 ;;
        --flannel-version) FLANNEL_VERSION="${2:-v0.15.1}"; shift 2 ;;
        *) echo "未知参数：$1"; exit 1 ;;
    esac
done

# 验证参数
if [[ -z "$MASTER_IP" || -z "$MASTER_USER" || -z "$MASTER_PASS" || -z "$WORKER_IPS" ]]; then
    echo "用法：$0 --master <ip> --masters-user <user> --masters-pass <pass> --worker <ip1,ip2,...> --workers-user <user> --workers-pass <pass>"
    exit 1
fi

log_info "=== K3s 集群自动化部署 ==="
log_info "Master: $MASTER_IP ($MASTER_USER)"
log_info "Workers: $WORKER_IPS ($WORKER_USER)"

# SSH 辅助函数
ssh_exec() {
    local host=$1
    local user=$2
    local pass=$3
    local cmd=$4
    
    echo "$pass" | sshpass -e ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 ${user}@${host} "$cmd"
}

# 检测网络接口
detect_interface() {
    local host=$1
    local user=$2
    local pass=$3
    
    ssh_exec $host $user $pass "ip route | grep default | awk '{print \$5}'" | head -1
}

# 预拉取镜像
pull_images() {
    local host=$1
    local user=$2
    local pass=$3
    
    log_info "在 $host 上拉取镜像..."
    
    local images=(
        "swr.cn-north-4.myhuaweicloud.com/ddn-k8s/quay.io/coreos/flannel:v0.15.1"
        "registry.aliyuncs.com/google_containers/pause:3.9"
        "registry.aliyuncs.com/google_containers/coredns:v1.10.1"
        "registry.aliyuncs.com/google_containers/kube-proxy:v1.28.0"
    )
    
    for img in "${images[@]}"; do
        log_info "拉取：$img"
        ssh_exec $host $user $pass "docker pull $img || true"
    done
}

# 安装 Master 节点
install_master() {
    local host=$1
    local user=$2
    local pass=$3
    
    log_info "=== 安装 Master 节点 $host ==="
    
    # 检测网络接口
    local iface=$(detect_interface $host $user $pass)
    log_info "检测到网络接口：$iface"
    
    # 关闭 Swap
    ssh_exec $host $user $pass "swapoff -a && sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab"
    
    # 安装 K3s
    log_info "安装 K3s Server..."
    ssh_exec $host $user $pass "curl -sfL https://get.k3s.io | sh -s - server \
        --flannel-backend vxlan \
        --cluster-cidr 10.244.0.0/16 \
        --service-cidr 10.96.0.0/12 \
        --disable-network-policy \
        --kubelet-arg container-runtime-endpoint=unix:///var/run/containerd/containerd.sock \
        --kubelet-arg pod-infra-container-image=registry.aliyuncs.com/google_containers/pause:3.9"
    
    # 获取 Token
    local token=$(ssh_exec $host $user $pass "cat /var/lib/rancher/k3s/server/node-token")
    export K3S_TOKEN=$token
    log_info "集群 Token: ${token:0:20}..."
    
    # 复制 kubeconfig
    ssh_exec $host $user $pass "mkdir -p ~/.kube && cp /etc/rancher/k3s/k3s.yaml ~/.kube/config && \
        sed -i 's/127.0.0.1/0.0.0.0/g' ~/.kube/config && \
        sed -i 's/127.0.0.1/$host/g' ~/.kube/config"
    
    echo "$token" > /tmp/k3s-token.txt
    log_info "Master 节点安装完成"
}

# 安装 Worker 节点
install_worker() {
    local host=$1
    local user=$2
    local pass=$3
    local token=$4
    
    log_info "=== 安装 Worker 节点 $host ==="
    
    # 关闭 Swap
    ssh_exec $host $user $pass "swapoff -a && sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab"
    
    # 安装 K3s Agent
    log_info "安装 K3s Agent..."
    ssh_exec $host $user $pass "curl -sfL https://get.k3s.io | sh -s - agent \
        --server https://$MASTER_IP:6443 \
        --token $token \
        --kubelet-arg container-runtime-endpoint=unix:///var/run/containerd/containerd.sock \
        --kubelet-arg pod-infra-container-image=registry.aliyuncs.com/google_containers/pause:3.9"
    
    log_info "Worker 节点安装完成"
}

# 部署 Flannel
deploy_flannel() {
    local host=$1
    local user=$2
    local pass=$3
    local iface=$4
    
    log_info "=== 部署 Flannel 网络插件 ==="
    
    # 检测网络接口（如果未提供）
    if [[ -z "$iface" ]]; then
        iface=$(detect_interface $host $user $pass)
    fi
    log_info "使用网络接口：$iface"
    
    # 创建 Flannel 配置文件
    local flannel_yaml="/tmp/k3s-flannel.yml"
    
    cat > $flannel_yaml << EOF
---
kind: ConfigMap
apiVersion: v1
metadata:
  name: kube-flannel-cfg
  namespace: kube-system
data:
  cni-conf.json: |
    {
      "name": "cbr0",
      "cniVersion": "0.3.1",
      "plugins": [
        {
          "type": "flannel",
          "delegate": {
            "hairpinMode": true,
            "isDefaultGateway": true
          }
        },
        {
          "type": "portmap",
          "capabilities": {
            "portMappings": true
          }
        }
      ]
    }
  net-conf.json: |
    {
      "Network": "10.244.0.0/16",
      "Backend": {
        "Type": "vxlan"
      }
    }
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-flannel-ds
  namespace: kube-system
  labels:
    tier: node
    app: flannel
spec:
  selector:
    matchLabels:
      app: flannel
  template:
    metadata:
      labels:
        tier: node
        app: flannel
    spec:
      hostNetwork: true
      tolerations:
        - operator: Exists
          effect: NoSchedule
      serviceAccountName: flannel
      containers:
        - name: kube-flannel
          image: swr.cn-north-4.myhuaweicloud.com/ddn-k8s/quay.io/coreos/flannel:v0.15.1
          args:
            - --ip-masq
            - --kube-subnet-mgr
            - --iface=${iface}
          resources:
            requests:
              cpu: "100m"
              memory: "50Mi"
            limits:
              cpu: "100m"
              memory: "50Mi"
          securityContext:
            privileged: false
            capabilities:
              add: ["NET_ADMIN", "NET_RAW"]
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          volumeMounts:
            - name: run
              mountPath: /run
            - name: flannel-cfg
              mountPath: /etc/kube-flannel/
            - name: cni
              mountPath: /etc/cni/net.d
      volumes:
        - name: run
          hostPath:
            path: /run
        - name: cni
          hostPath:
            path: /etc/cni/net.d
        - name: flannel-cfg
          configMap:
            name: kube-flannel-cfg
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: flannel
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: flannel
rules:
  - apiGroups:
      - ""
    resources:
      - pods
    verbs:
      - get
  - apiGroups:
      - ""
    resources:
      - nodes
    verbs:
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - nodes/status
    verbs:
      - patch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: flannel
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: flannel
subjects:
  - kind: ServiceAccount
    name: flannel
    namespace: kube-system
EOF
    
    # 在所有节点上传配置文件并部署
    local all_nodes="$host"
    for worker in $(echo $WORKER_IPS | tr ',' ' '); do
        all_nodes="$all_nodes $worker"
    done
    
    for node in $all_nodes; do
        if [[ "$node" == "$host" ]]; then
            local nuser=$user
            local npass=$pass
        else
            local nuser=$WORKER_USER
            local npass=$WORKER_PASS
        fi
        
        log_info "在 $node 上创建 CNI 配置..."
        
        # 上传配置文件
        echo "$npass" | sshpass -e scp $flannel_yaml ${nuser}@${node}:/tmp/k3s-flannel.yml
        
        # 创建 CNI 配置文件
        ssh_exec $node $nuser $npass "cat > /etc/cni/net.d/10-flannel.conflist << 'CNIEOF'
{
  \"name\": \"cbr0\",
  \"cniVersion\": \"0.3.1\",
  \"plugins\": [
    {
      \"type\": \"flannel\",
      \"delegate\": {
        \"hairpinMode\": true,
        \"isDefaultGateway\": true
      }
    },
    {
      \"type\": \"portmap\",
      \"capabilities\": {
        \"portMappings\": true
      }
    }
  ]
}
CNIEOF"
    done
    
    # 在 Master 上部署
    log_info "部署 Flannel DaemonSet..."
    ssh_exec $host $user $pass "kubectl apply -f /tmp/k3s-flannel.yml"
    
    rm -f $flannel_yaml
}

# 健康检查
health_check() {
    local host=$1
    local user=$2
    local pass=$3
    
    log_info "=== 集群健康检查 ==="
    
    local max_wait=300
    local waited=0
    
    while [[ $waited -lt $max_wait ]]; do
        local ready_count=$(ssh_exec $host $user $pass "kubectl get nodes --no-headers | grep 'Ready' | wc -l")
        local total_count=$(ssh_exec $host $user $pass "kubectl get nodes --no-headers | wc -l")
        
        log_info "节点状态：$ready_count/$total_count Ready"
        
        if [[ $ready_count -eq $total_count ]]; then
            log_info "所有节点已就绪！"
            
            # 检查系统 Pod
            ssh_exec $host $user $pass "kubectl get pods -n kube-system"
            
            # 生成集群信息
            ssh_exec $host $user $pass "kubectl get nodes -o wide" > /tmp/cluster-info.txt
            log_info "集群信息已保存到 /tmp/cluster-info.txt"
            
            return 0
        fi
        
        log_warn "等待节点就绪... (已等待 ${waited}s)"
        sleep 10
        waited=$((waited + 10))
    done
    
    log_error "超时：部分节点未就绪"
    ssh_exec $host $user $pass "kubectl get nodes"
    return 1
}

# 主流程
main() {
    log_info "步骤 1: 在 Master 节点拉取镜像"
    pull_images $MASTER_IP $MASTER_USER $MASTER_PASS
    
    log_info "步骤 2: 在 Worker 节点拉取镜像"
    for worker in $(echo $WORKER_IPS | tr ',' ' '); do
        pull_images $worker $WORKER_USER $WORKER_PASS
    done
    
    log_info "步骤 3: 安装 Master 节点"
    install_master $MASTER_IP $MASTER_USER $MASTER_PASS
    
    # 等待 K3s 启动
    sleep 15
    
    log_info "步骤 4: 安装 Worker 节点"
    local token=$(cat /tmp/k3s-token.txt)
    for worker in $(echo $WORKER_IPS | tr ',' ' '); do
        install_worker $worker $WORKER_USER $WORKER_PASS $token
    done
    
    # 等待 Worker 加入
    sleep 15
    
    log_info "步骤 5: 部署 Flannel 网络"
    deploy_flannel $MASTER_IP $MASTER_USER $MASTER_PASS
    
    log_info "步骤 6: 健康检查"
    health_check $MASTER_IP $MASTER_USER $MASTER_PASS
    
    # 清理临时文件
    rm -f /tmp/k3s-token.txt
    
    log_info "=== 部署完成 ==="
}

# 执行主流程
main
