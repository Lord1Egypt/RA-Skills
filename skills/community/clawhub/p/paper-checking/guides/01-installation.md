# 安装指南

**适用场景**: 首次使用论文查重系统，需要下载、编译和运行

---

## 一、系统要求检查

### 目标
确保系统具备运行论文查重系统的基础环境

### 前置条件
- Windows 7及以上操作系统
- 可用内存1.5GB以上
- 32位操作系统不支持（仅支持64位）

### 检查环境

**AI执行说明**: AI将指导你检查系统环境

```powershell
# 检查Windows版本
winver

# 检查可用内存
systeminfo | findstr /C:"可用物理内存"

# 检查系统架构（应显示x64）
systeminfo | findstr /C:"系统类型"
```

**期望结果**:
- Windows 7或更高版本 ✅
- 可用内存 ≥ 1.5GB ✅
- 系统类型: x64 ✅

---

## 二、下载项目

### 方式1: 使用git clone

**AI执行说明**: AI可以执行下载命令

```bash
# 克隆项目
git clone https://github.com/tianlian0/paper_checking_system.git
cd paper_checking_system
```

### 方式2: 直接下载Release

```bash
# 从GitHub Release下载编译好的版本
# 访问: https://github.com/tianlian0/paper_checking_system/releases

# 或使用浏览器下载ZIP压缩包
```

---

## 三、安装依赖

### 必需依赖

**1. Visual Studio 2017及以上**

下载地址: https://visualstudio.microsoft.com/

安装时选择组件：
- .NET开发组件（必需）
- vc2015运行库（系统自带或单独安装）

**2. .NET Framework 4.6**

Windows 10及以上已内置，Windows 7需单独安装：
下载地址: https://dotnet.microsoft.com/download/dotnet-framework

**3. NuGet包管理器**

Visual Studio 2017及以上已内置

---

## 四、编译项目

### 使用Visual Studio编译

**AI执行说明**: AI将指导编译步骤

**步骤1: 打开项目**
```
1. 启动Visual Studio 2017+
2. 打开 → 项目/解决方案
3. 选择 paper_checking_system.sln
```

**步骤2: 编译项目**
```
1. 菜单栏 → 构建 → 生成解决方案
2. 或按快捷键 Ctrl+Shift+B
3. 等待编译完成（首次可能需要较长时间）
```

**步骤3: 检查编译结果**
```
输出窗口显示：
- "生成成功" → 编译成功
- 错误提示 → 需要修复依赖
```

### 编译常见问题

**问题1: Spire组件报错**

**原因**: NuGet包未下载完毕

**解决方案**:
```
1. 等待VS自动下载完成
2. 或手动打开NuGet包管理器
3. 工具 → NuGet包管理器 → 管理解决方案的NuGet包
4. 搜索并安装缺失的包
```

**问题2: 32位系统报错**

**原因**: 项目不支持32位操作系统

**解决方案**:
```
必须使用64位Windows系统
不支持32位系统
```

---

## 五、运行系统

### 启动查重系统

**AI执行说明**: AI将指导启动步骤

```bash
# 方式1: 从Visual Studio运行
# 按F5或点击"启动"按钮

# 方式2: 直接运行可执行文件
cd paper_checking_system/bin/Release
paper_checking.exe
```

**成功标志**:
- ✅ 查重系统界面正常显示
- ✅ 所有功能按钮可用
- ✅ 文件选择对话框可正常打开

---

## 六、下载预编译版本（推荐）

### 从Release下载

如不想自行编译，可下载预编译版本：

```bash
# 访问Release页面
https://github.com/tianlian0/paper_checking_system/releases

# 下载最新版本
# 开源版和商用版均可在Release下载
```

**优势**:
- ✅ 无需编译
- ✅ 依赖已打包
- ✅ 可直接运行

---

## 七、验证安装

### 功能验证

**AI执行说明**: AI将验证系统可用性

```bash
# 1. 启动系统
paper_checking.exe

# 2. 检查界面
# 应看到：比对库管理、纵向查重、横向查重等选项卡

# 3. 测试文件选择
点击"选择待查文件" → 能正常打开文件夹

# 4. 测试查重阈值设置
能设置1-99之间的整数值
```

**成功标志**:
- ✅ 系统正常启动
- ✅ 所有选项卡可见
- ✅ 文件选择功能正常
- ✅ 参数设置功能正常

---

## 完成确认

### 检查清单
- [ ] Windows系统64位
- [ ] 可用内存≥1.5GB
- [ ] Visual Studio已安装
- [ ] .NET Framework 4.6已安装
- [ ] 项目已下载
- [ ] 编译成功或下载预编译版
- [ ] 系统可正常启动

### 下一步
继续阅读 [快速开始](02-quickstart.md) 学习如何进行第一次查重