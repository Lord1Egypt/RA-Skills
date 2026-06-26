#!/usr/bin/env bash
# container_audit.sh — 容器安全审计脚本
# 支持：Docker/Podman 环境检查、运行容器审计、镜像安全扫描、网络/存储检查
# 用法:
#   bash scripts/container_audit.sh              — 全面审计
#   bash scripts/container_audit.sh runtime      — 运行时检查
#   bash scripts/container_audit.sh images       — 镜像安全检查
#   bash scripts/container_audit.sh network      — 网络检查
#   bash scripts/container_audit.sh storage      — 存储检查

# 参数解析（优先处理 --help/--version）
case "${1:-}" in
    --help|-h)
        echo "用法: bash $0 {all|runtime|images|network|storage}"
        echo ""
        echo "容器安全审计：运行时检查、镜像安全、网络/存储检查，支持 Docker/Podman。"
        echo ""
        echo "命令:"
        echo "  all      — 全面审计（默认）"
        echo "  runtime  — 运行时与容器安全检查"
        echo "  images   — 镜像安全检查"
        echo "  network  — 网络配置检查"
        echo "  storage  — 存储与卷检查"
        echo ""
        echo "选项:"
        echo "  --help, -h      显示此帮助信息"
        echo "  --version       显示版本信息"
        exit 0
        ;;
    --version)
        echo "container_audit.sh v3.0.2"
        exit 0
        ;;
esac

ACTION="${1:-all}"

# 颜色输出（非终端环境自动禁用，避免转义码泄露）
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' CYAN='' NC=''
fi

pass()  { echo -e "  ${GREEN}✅ PASS${NC}: $1"; }
warn()  { echo -e "  ${YELLOW}⚠️  WARN${NC}: $1"; }
fail()  { echo -e "  ${RED}❌ FAIL${NC}: $1"; }
info()  { echo -e "  ℹ️  INFO: $1"; }

divider() {
    echo ""
    echo "================================================================"
    echo "  $1"
    echo "================================================================"
}

TOTAL=0
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

check_pass()  { TOTAL=$((TOTAL+1)); PASS_COUNT=$((PASS_COUNT+1)); pass "$1"; }
check_warn()  { TOTAL=$((TOTAL+1)); WARN_COUNT=$((WARN_COUNT+1)); warn "$1"; }
check_fail()  { TOTAL=$((TOTAL+1)); FAIL_COUNT=$((FAIL_COUNT+1)); fail "$1"; }

# 检测容器运行时
RUNTIME=""
detect_runtime() {
    if command -v docker &>/dev/null && docker info &>/dev/null; then
        RUNTIME="docker"
    elif command -v podman &>/dev/null; then
        RUNTIME="podman"
    else
        RUNTIME="none"
    fi
}

# ==================== 运行时检查 ====================
cmd_runtime() {
    divider "1. 容器运行时"

    detect_runtime

    case "$RUNTIME" in
        docker)
            local ver
            ver=$(docker version --format '{{.Server.Version}}' 2>/dev/null)
            check_pass "Docker Engine: v$ver"

            # containerd
            if command -v containerd &>/dev/null; then
                info "containerd: $(containerd --version 2>/dev/null | awk '{print $3}')"
            fi

            # Docker Compose
            if docker compose version &>/dev/null; then
                local compose_ver
                compose_ver=$(docker compose version --short 2>/dev/null)
                check_pass "Docker Compose: v$compose_ver"
            elif command -v docker-compose &>/dev/null; then
                check_warn "使用旧版 docker-compose，建议升级到 Docker Compose V2"
            fi

            # BuildKit
            if docker buildx version &>/dev/null; then
                check_pass "Docker Buildx 可用"
            fi
            ;;
        podman)
            local ver
            ver=$(podman version --format '{{.Client.Version}}' 2>/dev/null)
            check_pass "Podman: v$ver"
            if command -v podman-compose &>/dev/null; then
                check_pass "podman-compose 可用"
            fi
            ;;
        none)
            check_fail "未检测到容器运行时（Docker/Podman）"
            return
            ;;
    esac

    divider "2. 守护进程配置"

    if [ "$RUNTIME" = "docker" ]; then
        # daemon.json
        local daemon_json="/etc/docker/daemon.json"
        if [ -f "$daemon_json" ]; then
            check_pass "daemon.json 存在"

            # live-restore
            if grep -q '"live-restore".*true' "$daemon_json" 2>/dev/null; then
                check_pass "live-restore 已启用"
            else
                check_warn "live-restore 未启用（建议启用以减少守护进程重启影响）"
            fi

            # 日志配置
            if grep -q '"log-driver"' "$daemon_json" 2>/dev/null; then
                local log_driver
                log_driver=$(python3 -c "import json; print(json.load(open('$daemon_json')).get('log-driver','未配置'))" 2>/dev/null)
                info "日志驱动: $log_driver"
            fi

            # 日志大小限制
            if grep -q '"max-size"' "$daemon_json" 2>/dev/null; then
                check_pass "日志大小限制已配置"
            else
                check_warn "未配置日志大小限制（可能导致磁盘占满）"
            fi

            # userland-proxy
            if grep -q '"userland-proxy".*false' "$daemon_json" 2>/dev/null; then
                check_pass "userland-proxy 已禁用（使用 iptables 转发）"
            fi
        else
            check_warn "daemon.json 不存在（使用默认配置）"
        fi

        # Docker socket 权限
        if [ -S /var/run/docker.sock ]; then
            local sock_perms
            sock_perms=$(stat -c '%a' /var/run/docker.sock 2>/dev/null)
            local sock_group
            sock_group=$(stat -c '%G' /var/run/docker.sock 2>/dev/null)
            if [ "$sock_perms" = "660" ]; then
                check_pass "Docker socket 权限: $sock_perms（组: $sock_group）"
            else
                check_warn "Docker socket 权限: $sock_perms（建议 660）"
            fi
        fi
    fi

    divider "3. 容器概览"

    local running stopped total_containers
    running=$($RUNTIME ps -q 2>/dev/null | wc -l)
    total_containers=$($RUNTIME ps -aq 2>/dev/null | wc -l)
    stopped=$((total_containers - running))

    info "运行中容器: $running"
    info "已停止容器: $stopped"
    info "容器总数: $total_containers"

    if [ "$stopped" -gt 10 ]; then
        check_warn "有 $stopped 个已停止容器，建议清理"
    fi

    divider "4. 容器安全审计"

    # 逐个检查运行中的容器
    while read -r name; do
        [ -z "$name" ] && continue
        echo ""
        echo -e "  ${CYAN}--- 容器: $name ---${NC}"

        # 检查是否以 root 运行
        local user
        user=$($RUNTIME inspect --format '{{.Config.User}}' "$name" 2>/dev/null)
        if [ -z "$user" ] || [ "$user" = "root" ] || [ "$user" = "0" ]; then
            check_warn "$name: 以 root 用户运行"
        else
            check_pass "$name: 以非 root 用户运行（$user）"
        fi

        # 检查特权模式
        local privileged
        privileged=$($RUNTIME inspect --format '{{.HostConfig.Privileged}}' "$name" 2>/dev/null)
        if [ "$privileged" = "true" ]; then
            check_fail "$name: 特权模式运行（严重安全风险）"
        else
            check_pass "$name: 非特权模式"
        fi

        # 检查 capabilities
        local cap_add
        cap_add=$($RUNTIME inspect --format '{{.HostConfig.CapAdd}}' "$name" 2>/dev/null)
        if [ "$cap_add" != "[]" ] && [ "$cap_add" != "<nil>" ] && [ -n "$cap_add" ]; then
            check_warn "$name: 添加了额外 capabilities: $cap_add"
        fi

        # 检查资源限制
        local mem_limit
        mem_limit=$($RUNTIME inspect --format '{{.HostConfig.Memory}}' "$name" 2>/dev/null)
        if [ "$mem_limit" = "0" ] || [ -z "$mem_limit" ]; then
            check_warn "$name: 未设置内存限制"
        else
            local mem_mb=$((mem_limit / 1024 / 1024))
            check_pass "$name: 内存限制 ${mem_mb}MB"
        fi

        local cpu_limit
        cpu_limit=$($RUNTIME inspect --format '{{.HostConfig.NanoCpus}}' "$name" 2>/dev/null)
        if [ "$cpu_limit" = "0" ] || [ -z "$cpu_limit" ]; then
            info "$name: 未设置 CPU 限制"
        fi

        # 检查重启策略
        local restart_policy
        restart_policy=$($RUNTIME inspect --format '{{.HostConfig.RestartPolicy.Name}}' "$name" 2>/dev/null)
        if [ "$restart_policy" = "no" ] || [ -z "$restart_policy" ]; then
            info "$name: 重启策略: $restart_policy"
        else
            check_pass "$name: 重启策略: $restart_policy"
        fi

        # 检查 PID 限制
        local pids_limit
        pids_limit=$($RUNTIME inspect --format '{{.HostConfig.PidsLimit}}' "$name" 2>/dev/null)
        if [ "$pids_limit" = "0" ] || [ "$pids_limit" = "-1" ] || [ -z "$pids_limit" ]; then
            info "$name: 未设置 PID 限制"
        fi

        # 检查健康检查
        local healthcheck
        healthcheck=$($RUNTIME inspect --format '{{.Config.Healthcheck}}' "$name" 2>/dev/null)
        if [ -z "$healthcheck" ] || [ "$healthcheck" = "<nil>" ]; then
            info "$name: 未配置健康检查"
        else
            check_pass "$name: 已配置健康检查"
        fi

        # 检查只读根文件系统
        local readonly_rootfs
        readonly_rootfs=$($RUNTIME inspect --format '{{.HostConfig.ReadonlyRootfs}}' "$name" 2>/dev/null)
        if [ "$readonly_rootfs" = "true" ]; then
            check_pass "$name: 只读根文件系统"
        fi

        # 检查 no-new-privileges
        local no_new_priv
        no_new_priv=$($RUNTIME inspect --format '{{range .HostConfig.SecurityOpt}}{{.}} {{end}}' "$name" 2>/dev/null)
        if echo "$no_new_priv" | grep -q "no-new-privileges"; then
            check_pass "$name: no-new-privileges 已启用"
        fi

    done < <($RUNTIME ps --format '{{.Names}}' 2>/dev/null)
}

# ==================== 镜像安全检查 ====================
cmd_images() {
    divider "镜像安全检查"

    detect_runtime
    if [ "$RUNTIME" = "none" ]; then
        check_fail "无容器运行时"
        return
    fi

    # 镜像统计
    local image_count
    image_count=$($RUNTIME images -q 2>/dev/null | wc -l)
    info "本地镜像总数: $image_count"

    # 磁盘占用
    local total_size
    total_size=$($RUNTIME system df 2>/dev/null | grep "Images" | awk '{print $3, $4}')
    info "镜像占用空间: $total_size"

    # 悬空镜像
    local dangling
    dangling=$($RUNTIME images -f "dangling=true" -q 2>/dev/null | wc -l)
    if [ "$dangling" -gt 0 ]; then
        check_warn "有 $dangling 个悬空镜像（dangling），建议清理"
    else
        check_pass "无悬空镜像"
    fi

    echo ""
    echo -e "  ${CYAN}--- 运行中容器使用的镜像 ---${NC}"

    while read -r img; do
        [ -z "$img" ] && continue

        # 检查是否使用 latest 标签
        if echo "$img" | grep -qE ":latest$" || ! echo "$img" | grep -q ":"; then
            check_warn "镜像 $img 使用 latest 标签（建议使用具体版本）"
        else
            check_pass "镜像 $img 使用具体版本标签"
        fi

        # 检查镜像年龄
        local created
        created=$($RUNTIME inspect --format '{{.Created}}' "$img" 2>/dev/null | cut -d'T' -f1)
        if [ -n "$created" ]; then
            local created_ts now_ts age_days
            created_ts=$(date -d "$created" +%s 2>/dev/null)
            now_ts=$(date +%s)
            if [ -n "$created_ts" ]; then
                age_days=$(( (now_ts - created_ts) / 86400 ))
                if [ "$age_days" -gt 180 ]; then
                    check_warn "镜像 $img 已 ${age_days} 天未更新（>180天）"
                else
                    info "镜像 $img 创建于 ${age_days} 天前"
                fi
            fi
        fi
    done < <($RUNTIME ps --format '{{.Image}}' 2>/dev/null | sort -u)

    # Trivy 扫描（如果可用）
    if command -v trivy &>/dev/null; then
        echo ""
        echo -e "  ${CYAN}--- Trivy 漏洞扫描 ---${NC}"
        while read -r img; do
            [ -z "$img" ] && continue
            info "扫描 $img ..."
            local crit high
            crit=$(trivy image --severity CRITICAL --quiet "$img" 2>/dev/null | grep -c "CRITICAL" || echo "0")
            high=$(trivy image --severity HIGH --quiet "$img" 2>/dev/null | grep -c "HIGH" || echo "0")
            if [ "$crit" -gt 0 ]; then
                check_fail "$img: $crit 个 CRITICAL 漏洞"
            elif [ "$high" -gt 0 ]; then
                check_warn "$img: $high 个 HIGH 漏洞"
            else
                check_pass "$img: 无高危漏洞"
            fi
        done < <($RUNTIME ps --format '{{.Image}}' 2>/dev/null | sort -u | head -5)
    else
        info "Trivy 未安装（建议安装进行漏洞扫描）"
    fi
}

# ==================== 网络检查 ====================
cmd_network() {
    divider "容器网络检查"

    detect_runtime
    if [ "$RUNTIME" = "none" ]; then
        check_fail "无容器运行时"
        return
    fi

    # 网络列表
    local net_count
    net_count=$($RUNTIME network ls -q 2>/dev/null | wc -l)
    info "网络总数: $net_count"

    while IFS=$'\t' read -r name driver; do
        info "网络: $name（驱动: $driver）"
    done < <($RUNTIME network ls --format '{{.Name}}\t{{.Driver}}' 2>/dev/null)

    # 检查暴露端口
    echo ""
    echo -e "  ${CYAN}--- 端口映射 ---${NC}"
    while IFS=$'\t' read -r name ports; do
        [ -z "$ports" ] && continue
        # 检查是否绑定到 0.0.0.0
        if echo "$ports" | grep -q "0.0.0.0:"; then
            check_warn "$name: 端口绑定到所有接口（0.0.0.0）: $ports"
        else
            info "$name: $ports"
        fi
    done < <($RUNTIME ps --format '{{.Names}}\t{{.Ports}}' 2>/dev/null)

    # 检查 Docker socket 挂载
    echo ""
    echo -e "  ${CYAN}--- Docker Socket 检查 ---${NC}"
    while read -r name; do
        local mounts
        mounts=$($RUNTIME inspect --format '{{range .Mounts}}{{.Source}} {{end}}' "$name" 2>/dev/null)
        if echo "$mounts" | grep -q "docker.sock"; then
            check_fail "$name: 挂载了 Docker socket（容器逃逸风险）"
        fi
    done < <($RUNTIME ps --format '{{.Names}}' 2>/dev/null)
}

# ==================== 存储检查 ====================
cmd_storage() {
    divider "容器存储检查"

    detect_runtime
    if [ "$RUNTIME" = "none" ]; then
        check_fail "无容器运行时"
        return
    fi

    # 系统磁盘使用
    echo -e "  ${CYAN}--- 磁盘使用概览 ---${NC}"
    $RUNTIME system df 2>/dev/null

    # 卷管理
    echo ""
    local vol_count
    vol_count=$($RUNTIME volume ls -q 2>/dev/null | wc -l)
    info "卷总数: $vol_count"

    # 未使用的卷
    local unused_vols
    unused_vols=$($RUNTIME volume ls -f "dangling=true" -q 2>/dev/null | wc -l)
    if [ "$unused_vols" -gt 0 ]; then
        check_warn "有 $unused_vols 个未使用的卷，建议清理"
    else
        check_pass "无未使用的卷"
    fi

    # 检查 bind mount 权限
    echo ""
    echo -e "  ${CYAN}--- 挂载检查 ---${NC}"
    while read -r name; do
        while read -r mount_info; do
            [ -z "$mount_info" ] && continue
            local mtype msrc mdst mrw
            mtype=$(echo "$mount_info" | cut -d: -f1)
            msrc=$(echo "$mount_info" | cut -d: -f2)
            mdst=$(echo "$mount_info" | cut -d: -f3)
            mrw=$(echo "$mount_info" | cut -d: -f4)

            if [ "$mtype" = "bind" ]; then
                # 检查敏感目录挂载
                case "$msrc" in
                    /|/etc|/root|/var/run/docker.sock|/proc|/sys)
                        check_fail "$name: 挂载了敏感路径 $msrc → $mdst"
                        ;;
                    *)
                        if [ "$mrw" = "true" ]; then
                            info "$name: bind mount $msrc → $mdst (读写)"
                        else
                            check_pass "$name: bind mount $msrc → $mdst (只读)"
                        fi
                        ;;
                esac
            fi
        done < <($RUNTIME inspect --format '{{range .Mounts}}{{.Type}}:{{.Source}}:{{.Destination}}:{{.RW}} {{end}}' "$name" 2>/dev/null | tr ' ' '\n')
    done < <($RUNTIME ps --format '{{.Names}}' 2>/dev/null)

    # 构建缓存
    echo ""
    if [ "$RUNTIME" = "docker" ]; then
        local build_cache
        build_cache=$(docker system df 2>/dev/null | grep "Build Cache" | awk '{print $3, $4}')
        if [ -n "$build_cache" ]; then
            info "构建缓存: $build_cache"
        fi
    fi
}

# ==================== 汇总 ====================
print_summary() {
    echo ""
    echo "================================================================"
    echo "  审计汇总"
    echo "================================================================"
    echo "  总计: $TOTAL 项检查"
    echo -e "  ${GREEN}✅ 通过${NC}: $PASS_COUNT"
    echo -e "  ${YELLOW}⚠️  警告${NC}: $WARN_COUNT"
    echo -e "  ${RED}❌ 失败${NC}: $FAIL_COUNT"
    echo ""

    if [ "$FAIL_COUNT" -gt 0 ]; then
        echo -e "  ${RED}⚠️  发现 $FAIL_COUNT 个安全问题，请尽快修复${NC}"
        exit 1
    elif [ "$WARN_COUNT" -gt 0 ]; then
        echo -e "  ${YELLOW}👍 无严重问题，建议关注警告项${NC}"
        exit 0
    else
        echo -e "  ${GREEN}🎉 所有检查通过${NC}"
        exit 0
    fi
}

# ==================== 主入口 ====================
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          容器安全审计报告                                   ║"
echo "║          检查时间: $(date '+%Y-%m-%d %H:%M:%S')                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"

case "$ACTION" in
    runtime) cmd_runtime; print_summary ;;
    images)  cmd_images; print_summary ;;
    network) cmd_network; print_summary ;;
    storage) cmd_storage; print_summary ;;
    all)
        cmd_runtime
        cmd_images
        cmd_network
        cmd_storage
        print_summary
        ;;
    *)
        echo "用法: $0 {all|runtime|images|network|storage}"
        echo ""
        echo "  all      — 全面审计（默认）"
        echo "  runtime  — 运行时与容器安全检查"
        echo "  images   — 镜像安全检查"
        echo "  network  — 网络配置检查"
        echo "  storage  — 存储与卷检查"
        exit 1
        ;;
esac
