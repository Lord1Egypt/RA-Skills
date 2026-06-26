# 工具安装指南

**目标：** 安装顶刊级系统发育树分析所需的全部工具

---

## 📦 安装清单

| 工具 | 版本 | 用途 | 状态 |
|------|------|------|------|
| IQ-TREE | 3.1.1 | 最大似然建树 + ModelFinder + UFBoot2 | ✅ |
| trimAl | 1.5 | 比对修剪 | ✅ |
| CD-HIT | 4.8.1 | 序列去冗余 | ✅ |
| HMMER | 3.4 | 保守域验证 | ✅ |
| MAFFT | 7.x | 多序列比对 | ✅ (系统已装) |
| FastTree | 2.x | 快速建树（可选） | ✅ (系统已装) |
| R | 4.3.3 | 统计分析和可视化 | ✅ |
| ggtree | 3.10.1 | 发表级树可视化 | ✅ |
| patchwork | 1.3.2 | 多面板组合 | ✅ |

---

## 🔧 安装步骤

### 前置条件

确保有 conda 环境（推荐 Miniconda 或 Anaconda）

### Step 1: 修复 conda solver 问题 ⚠️

**问题：** conda 可能配置了 libmamba solver 但未正确安装，导致所有 conda 命令报错

```bash
# 错误信息
Error while loading conda entry point: conda-libmamba-solver 
(module 'libmambapy' has no attribute 'QueryFormat')
CondaValueError: You have chosen a non-default solver backend (libmamba) 
but it was not recognized. Choose one of: classic
```

**解决方案：**

```bash
# 方法 1: 修改配置文件（推荐）
sed -i 's/solver: libmamba/solver: classic/' ~/.condarc

# 方法 2: 手动编辑
vim ~/.condarc
# 将 solver: libmamba 改为 solver: classic

# 验证
cat ~/.condarc | grep solver
# 应该显示: solver: classic
```

### Step 2: 创建或激活 R 4.3 环境

```bash
# 如果已有 r43 环境，跳过此步
conda create -n r43 -c conda-forge r-base=4.3 -y

# 激活环境
conda activate r43
```

### Step 3: 安装生物信息学工具

```bash
# 安装 IQ-TREE（最重要）
conda install -n r43 -c bioconda iqtree -y

# 安装 trimAl
conda install -n r43 -c bioconda trimal -y

# 安装 CD-HIT
conda install -n r43 -c bioconda cd-hit -y

# 安装 HMMER（可选，用于域验证）
conda install -n r43 -c bioconda hmmer -y
```

**注意事项：**
- 每个工具安装需要 30 秒 - 2 分钟
- IQ-TREE 包较大（~4 MB），下载可能较慢
- 如果网络慢，可以配置清华镜像源

### Step 4: 安装 R 包

```bash
# 安装 ggtree（Bioconductor 包）
conda run -n r43 R --quiet --no-save -e '
if (!requireNamespace("BiocManager", quietly = TRUE)) 
  install.packages("BiocManager", repos="https://mirrors.tuna.tsinghua.edu.cn/CRAN/")
BiocManager::install("ggtree", update=FALSE, ask=FALSE)
'

# 安装其他 R 包（用 conda 安装更稳定）
conda install -n r43 -c conda-forge r-patchwork r-scales -y
```

**常见问题：**

**问题 1：** 从 CRAN 安装 R 包时报错缺少系统库（curl, png, xml2）

```
ERROR: dependencies 'curl', 'png', 'xml2' are not available
```

**解决方案：** 用 conda 安装 R 包而不是 CRAN

```bash
# ❌ 不推荐（可能缺依赖）
R -e 'install.packages("patchwork")'

# ✅ 推荐（自动处理依赖）
conda install -n r43 -c conda-forge r-patchwork -y
```

**问题 2：** ggtree 安装时间长（5-10 分钟）

**原因：** ggtree 依赖很多包，需要编译

**解决方案：** 耐心等待，或者用 conda 安装预编译版本

```bash
# 如果 BiocManager 安装太慢，可以试试 conda
conda install -n r43 -c bioconda bioconductor-ggtree -y
```

### Step 5: 验证安装

```bash
# 激活环境
conda activate r43

# 验证生物信息学工具
iqtree --version          # 应显示 IQ-TREE version 3.1.1
trimal --version          # 应显示 trimAl v1.5
cd-hit --version          # 应显示 CD-HIT version 4.8.1
hmmsearch -h | head -3    # 应显示 HMMER 3.4

# 验证 R 包
R --quiet --no-save -e 'library(ggtree); library(patchwork); cat("✅ All R packages loaded\n")'
# 应显示: ✅ All R packages loaded
```

---

## 🎯 快速安装脚本

如果你想一键安装所有工具，可以使用以下脚本：

```bash
#!/bin/bash
# 文件名: install_phylo_tools.sh

set -e  # 遇到错误立即退出

echo "=== PhyloTree 工具安装脚本 ==="

# Step 1: 修复 conda solver
echo "[1/5] 修复 conda solver..."
sed -i 's/solver: libmamba/solver: classic/' ~/.condarc 2>/dev/null || true

# Step 2: 创建环境（如果不存在）
echo "[2/5] 检查 R 环境..."
if ! conda env list | grep -q "^r43 "; then
    echo "创建 r43 环境..."
    conda create -n r43 -c conda-forge r-base=4.3 -y
fi

# Step 3: 安装生物信息学工具
echo "[3/5] 安装生物信息学工具..."
conda install -n r43 -c bioconda iqtree trimal cd-hit hmmer -y

# Step 4: 安装 R 包
echo "[4/5] 安装 R 包..."
conda run -n r43 R --quiet --no-save -e '
if (!requireNamespace("BiocManager", quietly = TRUE)) 
  install.packages("BiocManager", repos="https://mirrors.tuna.tsinghua.edu.cn/CRAN/")
BiocManager::install("ggtree", update=FALSE, ask=FALSE)
'
conda install -n r43 -c conda-forge r-patchwork r-scales -y

# Step 5: 验证
echo "[5/5] 验证安装..."
conda run -n r43 iqtree --version | head -1
conda run -n r43 trimal --version
conda run -n r43 R --quiet --no-save -e 'library(ggtree); cat("✅ ggtree loaded\n")'

echo ""
echo "✅ 所有工具安装完成！"
echo ""
echo "使用方法："
echo "  conda activate r43"
echo "  python3 /path/to/phylo-tree/scripts/run.py --query 'enzyme name'"
```

**使用方法：**

```bash
# 保存脚本
cat > install_phylo_tools.sh << 'EOF'
# ... 粘贴上面的脚本内容 ...
EOF

# 添加执行权限
chmod +x install_phylo_tools.sh

# 运行
./install_phylo_tools.sh
```

---

## 📊 安装时间估算

| 步骤 | 时间 |
|------|------|
| 修复 conda solver | < 1 秒 |
| 创建 R 环境（如需要） | 2-5 分钟 |
| 安装生物信息学工具 | 3-5 分钟 |
| 安装 R 包 | 5-10 分钟 |
| 验证 | < 1 分钟 |
| **总计** | **10-20 分钟** |

---

## 🐛 常见问题排查

### 问题 1: conda 命令报错

**症状：**
```
Error while loading conda entry point: conda-libmamba-solver
```

**解决：** 参考 Step 1 修复 solver 配置

### 问题 2: IQ-TREE 命令找不到

**症状：**
```
iqtree2: command not found
```

**原因：** IQ-TREE 3.x 的命令名是 `iqtree` 而不是 `iqtree2`

**解决：**
```bash
# ✅ 正确
iqtree --version

# ❌ 错误
iqtree2 --version
```

### 问题 3: R 包加载失败

**症状：**
```
Error: package 'ggtree' is not installed
```

**解决：**
```bash
# 重新安装
conda run -n r43 R -e 'BiocManager::install("ggtree", force=TRUE)'
```

### 问题 4: 网络下载慢

**解决：** 配置清华镜像源

```bash
# 添加到 ~/.condarc
cat >> ~/.condarc << 'EOF'
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
  - defaults
show_channel_urls: true
EOF
```

---

## ✅ 安装完成检查清单

运行以下命令，确保所有输出都正常：

```bash
# 1. IQ-TREE
conda run -n r43 iqtree --version
# 预期: IQ-TREE version 3.1.1

# 2. trimAl
conda run -n r43 trimal --version
# 预期: trimAl v1.5

# 3. CD-HIT
conda run -n r43 cd-hit --version
# 预期: CD-HIT version 4.8.1

# 4. HMMER
conda run -n r43 hmmsearch -h | head -1
# 预期: # hmmsearch :: search profile(s) against a sequence database

# 5. R 包
conda run -n r43 R --quiet --no-save -e '
library(ggtree)
library(patchwork)
library(ape)
library(phangorn)
library(ggplot2)
cat("✅ All packages loaded successfully\n")
'
# 预期: ✅ All packages loaded successfully
```

如果所有命令都正常输出，恭喜你！环境配置完成，可以开始使用 PhyloTree skill 了。

---

## 📚 工具文档链接

- **IQ-TREE:** http://www.iqtree.org/doc/
- **trimAl:** http://trimal.cgenomics.org/
- **CD-HIT:** http://weizhong-lab.ucsd.edu/cd-hit/
- **HMMER:** http://hmmer.org/
- **ggtree:** https://yulab-smu.top/treedata-book/
- **patchwork:** https://patchwork.data-imaginist.com/

---

**最后更新：** 2026-04-23  
**测试环境：** Ubuntu 22.04, Miniconda3, R 4.3.3
