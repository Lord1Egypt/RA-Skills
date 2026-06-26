---
name: kernel-vuln-discover
description: Linux 内核漏洞主动发现技能。当用户需要以下操作时使用此技能：(1) 对 Linux 内核特定子系统（io_uring、Netfilter、SMB、OverlayFS 等）进行漏洞挖掘；(2) 使用 fuzzer（syzkaller/trinity）对内核进行模糊测试；(3) 对内核代码进行静态审计和代码审查；(4) 基于 CVE 样本归纳发现模式并扫描同类漏洞；(5) 生成漏洞发现报告（PoC/根因分析）。不用于已知 CVE 查询（那是 kernel-cve-tracker 的职责）。
---

# Kernel Vulnerability Discovery

主动发现 Linux 内核未知漏洞的系统化方法论。

## 核心原则

1. **攻击面枚举优先** — 明确目标子系统的入口点、数据流、调用链
2. **已知 CVE 作为种子** — 从已修复 CVE 反推发现模式，扫描同类漏洞
3. **fuzzer + 人工审计协同** — 自动化发现异常，人工确认根因
4. **PoC 即交付** — 发现不等于完成，需要可验证的复现步骤

## 发现方法总览

| 方法 | 适用场景 | 工具/资源 |
|------|---------|----------|
| **CVE 模式归纳扫描** | 快速发现同类漏洞 | grep/awk + 正则模式库 |
| **Fuzzing** | 未知的内存错误、协议边界问题 | syzkaller、trinity、libfuzzer |
| **静态代码审计** | 逻辑漏洞、权限检查绕过 | Coccinelle、semgrep、grep |
| **代码差异分析** | upstream commit 引入的新漏洞 | git log、diff 分析 |
| **威胁模型驱动审计** | 有目标性地挖特定类型的漏洞 | STRIDE、PASTA 方法论 |

## Phase 1: 攻击面枚举

### 目标子系统清单（按漏洞密度排序）

```
高危：
- io_uring（异步 I/O，攻击面大）
- Netfilter（网络包处理，协议解析）
- SMB（网络文件系统，文件操作）
- OverlayFS（命名空间、权限）
- BPF（沙箱执行）
- TLS/XFRM（加密层）

中危：
- Ext4/BTRFS（文件系统）
- NVME（块设备）
- USB/HID（外设驱动）
- Bluetooth（无线协议栈）
```

### 入口点分析方法

```
1. 找到 syscalls 对应的 kernel 入口
   → grep -r "SYSCALL_DEFINE" vmlinux.h | grep <subsystem>

2. 找到 netlink/ops 注册点
   → grep -r "register_pernet_subsys\|nf_register_hook"
   
3. 找到 ioctl/字符设备入口
   → grep -r "struct file_operations\|.unlocked_ioctl"
```

## Phase 2: CVE 模式归纳扫描

### 已知漏洞模式库（来自 kernel-cve-tracker 参考数据）

**模式 A：权限检查绕过（OverlayFS）**
```
CVE-2023-2640 / CVE-2023-32629
根因：overlayfs_copy_up_meta_pages / overlayfs_rename
触发条件：跨层命名空间操作时未校验 upper/lower layer 关系
审计关键词：
  - overlayfs_rename
  - overlayfs_getattr
  - overlayfs_permission
  - check_upper_layer / check_lower_layer
```

**模式 B：in-place 加密操作处理不当（algif_aead）**
```
CVE-2026-31431 (Copy Fail)
根因：aead 加密时 src/dst 同一 buffer，未正确处理复制
触发条件：crypto_aead_encrypt / crypto_aead_decrypt
审计关键词：
  - "src == dst"
  - "in-place"
  - aead_encrypt + aead_decrypt
  - "Copy Fail"
```

**模式 C：io_uring 内存错误**
```
CVE-2026-23351（io_uring 子系统）
根因：ring 内存映射操作时未校验 buffer 大小
审计关键词：
  - io_uring_enter
  - io_sqring_enter
  - "mmap" + "ring"
  - "fixed buffers"
```

**模式 D：Netfilter 整数溢出/越界**
```
CVE-2026-23274（Netfilter）
根因：nf_tables 表达式解析时整数溢出
审计关键词：
  - nf_register_hook
  - nf_tables_newrule
  - "int overflow" / "shift overflow"
  - "nft_expr"
```

**模式 E：SMB 协议解析边界错误**
```
CVE-2024-50060（SMB）
根因：smb2_negotiate / smb2_read 缺少长度校验
审计关键词：
  - smb2_read / smb2_write
  - "pdu_length" / "buffer length"
  - "size check missing"
```

### 扫描脚本（见 scripts/cve-pattern-scan.sh）

```bash
#!/bin/bash
# 用法：./cve-pattern-scan.sh <kernel-source-path> <pattern-name>
# 示例：./cve-pattern-scan.sh /path/to/linux-5.15 "aead_copy_fail"

KERNEL_PATH="$1"
PATTERN="$2"

case "$PATTERN" in
  aead_copy_fail)
    grep -rn "in-place\|src.*dst\|aead_encrypt" "$KERNEL_PATH/crypto/af_alg.c"
    ;;
  overlayfs_priv)
    grep -rn "overlayfs_rename\|overlayfs_getattr\|check_upper_layer" "$KERNEL_PATH/fs/overlayfs/"
    ;;
  io_uring_ring)
    grep -rn "mmap.*ring\|fixed.*buffer\|io_uring_enter" "$KERNEL_PATH/fs/io_uring/"
    ;;
  netfilter_overflow)
    grep -rn "nf_tables\|shift.*overflow\|integer.*overflow" "$KERNEL_PATH/net/netfilter/"
    ;;
esac
```

## Phase 3: Fuzzing

### syzkaller 工作流

```bash
# 1. 构建 syzkaller
go get github.com/google/syzkaller
cd $GOPATH/src/github.com/google/syzkaller

# 2. 生成 kernel config（启用 KCOV、KMEMLEAK、UBSAN）
cd /path/to/linux-5.15
make kvmconfig5_15 > /tmp/.kconfig
make KCONFIG_CONFIG=/tmp/.kconfig kvmconfig5_15

# 3. 编译内核（KCOV + DEBUG）
cd /path/to/linux-5.15
make KCONFIG_CONFIG=/tmp/.kconfig \
  KCFLAGS="-fsanitize=kernel-address" \
  -j$(nproc)

# 4. 编写 syz-manager 配置
cat > /tmp/syz-config.yaml << 'EOF'
project: linux
kernel_dir: /path/to/linux-5.15
kernel_config: /tmp/.kconfig
type: gce
vm:
  count: 4
  cpu: 4
  memory: 8
EOF

# 5. 启动 fuzzing
./bin/syz-manager -config /tmp/syz-config.yaml
```

### Trinity（轻量级 fuzzer）

```bash
# Trinity：覆盖所有 syscalls 的随机 fuzzer
git clone https://github.com/kernelsploit/trinity
cd trinity
./configure --quiet
make -j$(nproc)
./trinity -q   # quiet mode，不输出正常调用
./trinity -l 1000 -q  # 限制 1000 次系统调用后退出
./trinity -e 'read,write,ioctl,mmap'  # 指定只 fuzz 这些 syscall
```

### libfuzzer（单目标 harness）

```c
// 示例：fuzz io_uring_setup
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < sizeof(struct io_uring_params)) return 0;
    struct io_uring_params params;
    memcpy(&params, data, sizeof(params));
    
    // 边界条件：flags=0、depth=0、params 包含异常值
    int fd = syscall(SYS_io_uring_setup, params.entries, &params);
    if (fd >= 0) close(fd);
    return 0;
}
```

编译：
```bash
clang -fsanitize=address,fuzzer -o io_uring_fuzz io_uring_fuzz.c
```

## Phase 4: 静态代码审计

### Cocciinelle（语义 patch）

```bash
# 安装
apt install coccinelle

# 检查 use-after-free
@r exists@
local idexpression struct file *filp;
expression f;
@@

f = fget(...);
... when != f = fput(...);
- fput(f);
+ // 删除了 fput，导致 f 继续被使用
```

### semgrep（结构化扫描）

```bash
# 安装 semgrep
pip install semgrep

# 扫描 kernel 代码
semgrep --config auto /path/to/linux/fs/io_uring/

# 自定义规则：检查 copy_from_user 未校验返回值
rules:
  - id: unchecked-copy-from-user
    pattern: |
      copy_from_user($DST, $SRC, $N);
    message: copy_from_user return value not checked
    severity: ERROR
    languages: [c]
```

## Phase 5: 代码差异分析

### 从 upstream commit 发现漏洞引入

```bash
# 1. 找到 CVE 对应的 upstream commit
# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/?id=<commit>

# 2. 分析 commit 改动范围
git show <commit> --stat

# 3. 检查是否有类似模式的其他代码
git log --all -p --grep="same pattern" -- <subsystem-dir>

# 4. 版本区间扫描
git log v5.10..v5.15 --oneline -- fs/overlayfs/ | head -50
```

## Phase 6: 漏洞报告格式

发现漏洞后，按以下格式输出：

```markdown
##漏洞标题（CVE 申请用）

### 基本信息
- **发现日期**：YYYY-MM-DD
- **发现者**：<名字>
- **漏洞类型**：CVE 类型分类（CWE-122/CWE-190 等）
- **影响子系统**：<subsystem>

### 根因分析
<详细的代码级根因描述，最好附上行号>

### 攻击路径
<从用户空间到触发漏洞的完整调用链>

### 触发条件
```
<最小复现步骤>
```

### PoC
```c
<完整可编译的 PoC 代码>
```

### 修复建议
<上游 patch 方向或临时缓解措施>

### 引用
- 相关 CVE：
- 相关 commit：
- 相关 CWE：
```

## 快速命令速查

```bash
# 内核源码下载（指定版本）
git clone --depth=1 git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git linux-5.15

# 编译特定模块
cd linux-5.15 && make fs/overlayfs/overlayfs.o -j$(nproc)

# 查找特定 CVE 的 upstream commit
git log --all --grep="CVE-2023-2640" --oneline

# 查找某子系统的所有 syscalls
grep -rn "SYSCALL_DEFINE" linux-5.15/fs/io_uring/ | head -20

# 检查内核配置（KCOV 是否启用）
zcat /proc/config.gz | grep -E "KCOV|KMEMLEAK|UBSAN"
```

## 参考数据

- 完整 CVE 模式库：`references/cve-patterns.md`
- 各子系统审计清单：`references/subsystem-checklists.md`
- 上游内核 commit 规律：`references/upstream-commits.md`