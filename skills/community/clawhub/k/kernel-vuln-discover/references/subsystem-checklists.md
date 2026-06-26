# 子系统审计清单

> 每个子系统的关键检查项，用于系统性审计。

---

## io_uring

### 入口点
- `io_uring_setup(2)` — ring 创建
- `io_uring_enter(2)` — 提交/等待操作
- `io_uring_register(2)` — 注册 buf/	eventfd

### 审计检查项

| # | 检查项 | 关键词/代码模式 | 风险 |
|---|-------|----------------|------|
| 1 | Ring buffer mmap 映射大小校验 | `io_uring_mmap` + `size < PAGE_SIZE` | 越界读取 |
| 2 | fixed buffer 与 user buffer 重叠检测 | `fixedbufs` + `ptr_eq(src,dst)` | 数据破坏 |
| 3 | sqe->opcode 有效性校验 | `if (opcode >= IORING_OP_LAST)` | 任意调用 |
| 4 | io_uring_submit 竞态条件 | `io_submit_sqes` + `uring_lock` | DoS |
| 5 | timeout/cmdc 越界 | `io_linked_timeout` + `off < 0` | 越界访问 |

### 常见根因模式
```c
// 错误：未校验 buf 数量上限
io_buffer_register(buf, nr_bufs, type);

// 正确：应该有上限检查
if (nr_bufs > UIO_MAXIOV) return -EINVAL;
```

---

## Netfilter

### 入口点
- `nf_register_hook(2)` — 注册包处理 hook
- `nf_tables_newrule(2)` — 创建 netfilter table 规则
- `nft_lookup` / `nft_payload` — 表达式解析

### 审计检查项

| # | 检查项 | 关键词/代码模式 | 风险 |
|---|-------|----------------|------|
| 1 | nft_expr 解析时整数溢出 | `shift << 32` / `nft_set_elem` | 越界写入 |
| 2 | nf_hook_slow 路径长度计算 | `hooknum + 1` / `nf_hook` | 跳过检查 |
| 3 | xt_target 边界条件 | `target->target` + `len < 0` | 绕过 |
| 4 | conntrack 内存耗尽 | `nf_conntrack_alloc` + `GFP_ATOMIC` | DoS |
| 5 | ebtables table 锁定竞态 | `xt_table.*lock` + `rcu_read_lock` | 条件竞争 |

### 常见根因模式
```c
// 危险：shift 未边界检查
shift = left << right;
if (shift >= 64) return -EOVERFLOW;

// 正确写法
if (right >= 64) return -EINVAL;
shift = (left << right) & ((1ULL << 64) - 1);
```

---

## SMB/CIFS

### 入口点
- `smb2_read` / `smb2_write` — 读写操作
- `smb2_negotiate` — 协议协商
- `cifs_mount` — 挂载操作

### 审计检查项

| # | 检查项 | 关键词/代码模式 | 风险 |
|---|-------|----------------|------|
| 1 | PDU 长度字段校验 | `pdu_length == data_len + header` | 缓冲区溢出 |
| 2 | unicode 字符串截断 | `strncpy` + `\0` 不对齐 | 信息泄露 |
| 3 | credit grant 溢出 | `credits.granted + credits.requested` | DoS |
| 4 | symlink 解析递归深度 | `unix_to_basic_fid` + `recurse_depth` | 栈溢出 |
| 5 | lease 版本不匹配 | `lease->version != SMB_LEASE_VERSION` | 逻辑漏洞 |

---

## OverlayFS

### 入口点
- `overlayfs_rename(2)`
- `overlayfs_getattr(2)`
- `overlayfs_permission(2)`

### 审计检查项

| # | 检查项 | 关键词/代码模式 | 风险 |
|---|-------|----------------|------|
| 1 | upper/lower 层目录交叉检查 | `ovl_path_upper` + `ovl_path_lower` | 权限绕过 |
| 2 | 跨层 rename 复制元数据 | `overlayfs_copy_up` + `ovl_copy_meta` | 数据破坏 |
| 3 | whiteout 处理 | `ovl_wh_type` + `origin` | 文件隐藏漏洞 |
| 4 | volatile 挂载安全 | `ovl_workdir_create` + `tmp` | 竞态条件 |

---

## BPF

### 入口点
- `bpf(2)` syscall — BPF 系统调用
- `bpf_prog_load` — 程序加载
- `bpf_map_lookup_elem` — Map 查询

### 审计检查项

| # | 检查项 | 关键词/代码模式 | 风险 |
|---|-------|----------------|------|
| 1 | 验证器指针类型追踪 | `check_ptr_alignment` | 沙箱绕过 |
| 2 | BPF_MAP 越界访问 | `map->ops->map_*_elem` | 任意读写 |
| 3 | Helper 函数签名绕过 | `check_func_arg` + `ARG_PTR_*` | 提权 |
| 4 | JIT spray 攻击 | `bpf_jit_enable` + `BPF_JIT` | 绕过 ASLR |

---

## Ext4

### 审计检查项

| # | 检查项 | 关键词/代码模式 | 风险 |
|---|-------|----------------|------|
| 1 | extent 块分配大小校验 | `ext4_ext_map_blocks` + `len > EXT_MAX_BLOCK` | 越界写入 |
| 2 | journal handle 引用计数 | `ext4_journal_start` + `blocks <= 0` | Use-after-free |
| 3 | fast symlink 截断 | `i_size != strlen` | 信息泄露 |
| 4 | ea_inode 循环引用 | `ext4_xattr_ibody_get` + `inode == current` | 递归 DoS |

---

## 通用内存相关审计模式

对所有子系统都适用的通用检查：

### 1. copy_from_user 返回值未检查
```c
// 危险
copy_from_user(to, from, n);

// 正确
if (copy_from_user(to, from, n) != 0) return -EFAULT;
```

### 2. 整数溢出（malloc 大小参数）
```c
// 危险
p = kmalloc(size + offset, GFP_KERNEL);

// 正确
if (size + offset < size) return -EINVAL;  // 溢出检测
p = kmalloc(size + offset, GFP_KERNEL);
```

### 3. use-after-free
```c
// 危险
fput(file);      // 释放
...             
fput(file);      // 再次使用

// 正确：每次使用前重新获取引用
file = fget(fd);
if (!file) return -EBADF;
...
fput(file);
```

### 4. 竞态条件（TOCTOU）
```c
// 危险：time-of-check to time-of-use
if (capable(CAP_SYS_ADMIN)) {
    // 释放 capability
    capable_set = false;
    // 此时另一线程可能已改变状态
    do_something_privileged();
}

// 正确：原子操作或锁保护
mutex_lock(&admin_lock);
if (capable(CAP_SYS_ADMIN)) {
    do_something_privileged();
}
mutex_unlock(&admin_lock);
```

---

## 审计工具速查

| 工具 | 用途 | 常用命令 |
|------|------|---------|
| `coccinelle` | 语义 patch 扫描 | `spatch --sp-file rules.cocci .` |
| `semgrep` | 结构化规则扫描 | `semgrep --config rules.yaml /path/` |
| `grep` | 快速关键词搜索 | `grep -rn "pattern" subsystem/` |
| ` pahole` | 结构体大小分析 | `pahole vmlinux` |
| `nm vmlinux` | 内核符号表 | `nm vmlinux \| grep "T io_uring"` |