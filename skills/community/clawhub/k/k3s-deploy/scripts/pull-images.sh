#!/bin/bash
# 预拉取 K3s 必要镜像
# 用法：./pull-images.sh <host> <user> <password>

set -e

HOST=$1
USER=$2
PASS=$3

if [[ -z "$HOST" || -z "$USER" || -z "$PASS" ]]; then
    echo "用法：$0 <host> <user> <password>"
    exit 1
fi

echo "=== 在 $HOST 上拉取 K3s 必要镜像 ==="

IMAGES=(
    "swr.cn-north-4.myhuaweicloud.com/ddn-k8s/quay.io/coreos/flannel:v0.15.1"
    "registry.aliyuncs.com/google_containers/pause:3.9"
    "registry.aliyuncs.com/google_containers/coredns:v1.10.1"
    "registry.aliyuncs.com/google_containers/kube-proxy:v1.28.0"
    "registry.aliyuncs.com/google_containers/etcd:3.5.9"
    "registry.aliyuncs.com/google_containers/pause:3.5"
)

for img in "${IMAGES[@]}"; do
    echo "拉取：$img"
    echo "$PASS" | sshpass -e ssh -o StrictHostKeyChecking=no ${USER}@${HOST} "docker pull $img || echo '失败：$img'"
done

echo "=== 镜像拉取完成 ==="
echo "$PASS" | sshpass -e ssh -o StrictHostKeyChecking=no ${USER}@${HOST} "docker images"
