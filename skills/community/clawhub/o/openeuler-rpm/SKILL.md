---
name: openeuler-rpm
category: packaging
description: "🚨 openEuler 专项 RPM 打包规范。任何涉及 openEuler 打包的场景，都必须读取此技能。**openEuler 规则与通用 RPM 不同**：5 包拆分规则、专用 changelog 格式（Type/ID/SUG/DESC）、openEuler 专用宏、检视原则。不适用于其他发行版。"
version: 2.1.0
metadata: {"openclaw":{"requires":{"skills":["rpm"]}}}
---

# openEuler RPM 打包技能 — openEuler 打包规范的唯一来源

> ⚠️ **核心规则：**
> 
> **openEuler 的打包规则与通用 RPM 有显著差异。通用 RPM 知识不够用。**
> 
> **差异包括：5 包拆分规则、专用 changelog 格式（Type/ID/SUG/DESC 四字段）、openEuler 专用宏（%disable_rpath, %delete_la_and_a 等）、检视原则。这些在通用 RPM 文档中都不存在。**
> 
> **因此：任何 openEuler 打包场景，都必须读取此技能。绝不能用通用 RPM 知识代替。**

## 🚨 触发规则 — 遇到以下任何情况，立即读取此技能

| 如果你要做… | 你应该… | 禁止行为 |
|---|---|---|
| 为 openEuler 编写/修改 spec | ✅ 读取此技能 | ❌ 用通用 RPM 模板 |
| 拆分 openEuler 子包（libs/devel/static/help） | ✅ 读取此技能 | ❌ 按 Fedora/CentOS 方式拆分 |
| 写 openEuler changelog | ✅ 读取此技能 | ❌ 用通用 changelog 格式（必须用 Type/ID/SUG/DESC） |
| 使用 openEuler 专用宏 | ✅ 读取此技能 | ❌ 凭记忆写 %disable_rpath 等宏 |
| openEuler 包检视/审查 | ✅ 读取此技能 | ❌ 用通用标准检查 |
| 处理 openEuler 补丁命名 | ✅ 读取此技能 | ❌ 用其他发行版的补丁命名规则 |
| 判断 openEuler 架构支持 | ✅ 读取此技能 | ❌ 凭记忆写 ExcludeArch |
| openEuler 包升级 | ✅ 读取此技能 | ❌ 直接改版本号不更新 changelog |

### 如何判断该读哪个技能？

| 发行版 | 读取技能 |
|---|---|
| **openEuler** | `openeuler-rpm`（同时自动获得 `rpm` 能力） |
| Fedora / CentOS / RHEL | `rpm`（通用 RPM） |
| 不确定是哪个发行版 | **两个都读** |

### 快速自检

当你要为 **openEuler** 编写或修改 **任何 spec 文件、changelog、子包拆分、宏使用** 时，问自己：

> "openEuler 的 changelog 格式是什么？包拆分规则是什么？专用宏怎么用？"

如果不确定 → **读取此技能**。

---

## 🎯 核心原则

**openEuler 打包原则：不做复杂的拆分，将软件拆分为基本固定的 5 个 RPM 包，保持包的简洁。**

## 📦 包拆分规则

openEuler 标准包结构（5 个）：

| 包类型 | 包名 | 内容 | 关键点 |
|--------|------|------|--------|
| **主包** | `mypackage` | 命令、配置、so、license、copyright、readme、man/info | 可通过 Provides/Obsoletes 兼容其他 OS |
| **libs 包** | `mypackage-libs` | 对外提供的动态库、命令 | 分离功能与能力，避免循环依赖 |
| **devel 包** | `mypackage-devel` | 头文件、Example、tests、开发内容 | devel 包需 Requires 主包 |
| **static 包** | `mypackage-static` | 静态库.a、静态版本 | 可使用宏控制 |
| **help 包** | `mypackage-help` | 二次开发文档、手册 | **文档大时才拆分** |

### 特殊拆分
- `for-language` 包：`python2-mypackage`、`python3-mypackage`、`perl-mypackage`
- 本地化支持：`mypackage-lang`（复杂国际化相关软件）
- 其他复杂包：gcc、python2、python3 等

---

## 📝 Spec 文件结构

### 标准模板（主包）
```spec
Name:           mypackage
Version:        1.0.0
Release:        1%{?dist}
Summary:        Package summary

License:        MIT
URL:            https://example.com
Source0:        https://github.com/%{url}/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
Requires:       glibc >= 2.17

# openEuler 补丁命名：PATCH-(BUGFIX|CVE|FEATURE)-内容
# Patch0:       PATCH-BUGFIX-fix-build.patch

%description
Detailed package description.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_test

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Tue Apr 7 2020 openEuler Buildteam <buildteam@openeuler.org> - 10.33-3
- Type: CVES
- ID: CVE-2019-20454
- SUG: NA
- DESC: fix CVE-2019-20454

* Wed Apr 15 2026 zhangsan <zhangsan@example.com> - 1.0.0-1
- Type: Feature
- ID: NA
- SUG: NA
- DESC: Initial packaging for openEuler
```

### multi-package 模板
```spec
# ——— 主包 ——————————————————————————————————————

Name:           mypackage
Version:        1.0.0
Release:        1%{?dist}
Summary:        Main package

License:        MIT
URL:            https://example.com
Source0:        https://github.com/%{url}/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
Requires:       %{name}-libs = %{version}-%{release}

%description
Main package containing commands, configs, and runtime libraries.

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*

# ——— libs 包 ——————————————————————————————————————

%package -n libs
Summary:        Libraries for %{name}
Requires:       %{name} = %{version}-%{release}

%description -n libs
Runtime libraries for %{name}.

%files -n libs
%{_libdir}/lib%{name}.so.*

# ——— devel 包 ——————————————————————————————————————

%package -n devel
Summary:        Development files for %{name}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}

%description -n devel
Development files for %{name}.

%files -n devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

# ——— static 包（可选） ——————————————————————————

%package -n static
Summary:        Static libraries for %{name}
Requires:       %{name}-devel = %{version}-%{release}

%description -n static
Static libraries for %{name}.

%files -n static
%{_libdir}/lib%{name}.a

# ——— help 包（可选，文档大时） ——————————————

%package -n help
Summary:        Documents for %{name}
BuildArch:      noarch
Requires:       man info

%description -n help
Man pages and other related documents for %{name}.

%files -n help
%{_datadir}/%{name}/doc/
```

---

## 🔧 openEuler 专用宏

```spec
# 删除 rpath
%disable_rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool \
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# 删除 .la 和 .a 文件
%delete_la_and_a
find $RPM_BUILD_ROOT -type f -name "*.la" -delete \
find $RPM_BUILD_ROOT -type f -name "*.a" -delete

# 删除 .la 文件
%delete_la
find $RPM_BUILD_ROOT -type f -name "*.la" -delete

# 删除 chrpath
%chrpath_delete
find $RPM_BUILD_ROOT/ -type f -exec file {} ';' | grep "<ELF>" | awk -F ':' '{print $1}' | xargs chrpath --delete {}

# help 子包定义
%package_help
%package        help \
Summary:        Documents for %{name} \
Buildarch:      noarch \
Requires:               man info

%description help \
Man pages and other related documents for %{name}.

# info 工具
%install_info()
/sbin/install-info %1 %{_infodir}/dir || :

%install_info_rm()
/sbin/install-info --remove %1 %{_infodir}/dir || :
```

---

## 📋 openEuler 专用规范

### 1. 来源可靠
- ❌ 不要内嵌预编译的二进制文件或库文件
- ❌ 避免多个上游项目捆绑到一个软件包
- ✅ 软件应该是开源软件
- ✅ spec 文件要适配 openEuler
- ❌ 黑名单软件**必须不能**引入

### 2. 架构支持
- 尽量支持 aarch64 和 x86_64 架构
- 架构强相关内容通过 `%ifarch` 宏控制
- 无架构内容构建成 noarch 包
- 使用 `ExcludeArch:` 或 `ExclusiveArch:` 控制

### 3. changelog 格式
openEuler 要求 changelog 使用特定格式（**必须严格遵守**）：

#### 3.1 标题行格式（必须）
```
* Day Mon DD YYYY 提交人 <邮箱> - [Epoch:]Version-Release
```

| 部分 | 说明 | 示例 |
|------|------|------|
| 日期 | 格式 `* 星期 月 日 年` | `* Wed Apr 15 2026` |
| 提交人 | 姓名（不带括号） | `zhangsan`、`lisi` |
| 邮箱 | 必须用尖括号包裹 | `<user@example.com>` |
| Epoch | **可选**，取决于 spec 是否定义了 `Epoch` 字段。若定义了必须写，否则不写 | `1:` |
| Version | 与 spec `Version` 一致 | `2.4.7` |
| Release | 修改后的 release 值 | `14` |

**完整示例：**
```spec
# 有 Epoch 的包（如 cups: Epoch: 1）
* Wed Apr 15 2026 zhangsan <zhangsan@example.com> - 1:2.4.7-13

# 没有 Epoch 的包（大多数）
* Tue Apr 7 2020 openEuler Buildteam <buildteam@openeuler.org> - 10.33-3
```

#### 3.2 内容行格式（CVES 类型必须包含 4 个字段）

**Type 字段取值：`CVES` / `Bugfix` / `Feature`**

**CVES（多个 CVE 修复）：**
```spec
* Wed Apr 15 2026 zhangsan <zhangsan@example.com> - 1:2.4.7-13
- Type: CVES
- ID: CVE-2026-27447 CVE-2026-34978 CVE-2026-34979
- SUG: NA
- DESC: fix CVE-2026-27447 CVE-2026-34978 CVE-2026-34979
```

**Bugfix（普通缺陷修复）：**
```spec
* Mon Mar 10 2026 lisi <lisi@example.com> - 1:2.4.7-12
- Type: Bugfix
- ID: NA
- SUG: NA
- DESC: fix build failure with gcc-15
```

**Feature（新增功能/版本升级）：**
```spec
* Sat Apr 25 2026 wangwu <wangwu@example.com> - 2.0.0-1
- Type: Feature
- ID: NA
- SUG: NA
- DESC: Update to 2.0.0
```

| 字段 | 取值 | 说明 |
|------|------|------|
| `Type` | `CVES` / `Bugfix` / `Feature` | CVES=多个CVE，Bugfix=普通修复，Feature=新功能 |
| `ID` | CVE-XXXX-XXXX 或 Bugzilla 编号 | CVE 修复必须写完整 CVE 编号 |
| `SUG` | `NA` 或具体建议 | 无特殊建议写 `NA` |
| `DESC` | 简短描述 | 说明做了什么 |

#### 3.3 常见错误（必须避免）
| 错误 | 正确 |
|------|------|
| `* Sat Apr 25 2026 zhangsan - 2.4.7-14`（缺 `<email>`、缺 epoch） | `* Sat Apr 25 2026 zhangsan <zhangsan@example.com> - 1:2.4.7-14` |
| `- fix CVE-2026-41079`（缺少 Type/ID/SUG/DESC） | `- Type: CVES\n- ID: CVE-2026-41079\n- SUG: NA\n- DESC: fix CVE-2026-41079` |
| `- Type: CVES/Bugfix/Feature`（不要写多个类型） | 每条 changelog 只写一个 Type 值（CVES 或 Bugfix 或 Feature） |
| 用 `your@email.com` 等占位邮箱 | 用实际邮箱，从 git config 或已有 changelog 获取 |

#### 3.4 修改 changelog 的标准流程（必须遵守）
1. **先查看 spec 是否定义了 `Epoch`** — `grep "^Epoch" xxx.spec`
2. **参考 spec 已有 changelog 条目的格式** — 看最新一条的写法（日期格式、邮箱格式、Epoch 有无）
3. **按已有格式风格写入新条目** — 不凭记忆，不自行编造格式

### 4. 命名规则
- 主包名称与软件名称同名
- 如多个版本：`mypackage2` 或 `mypackage-stable`
- 语言模块：`python-mypackage`、`perl-mypackage`
- 补丁命名：`PATCH-BUGFIX-fix-build.patch`

### 5. 依赖关系
- `Requires:` - 软件正常工作所需
- `Recommends:` / `Suggests:` - 非必需但推荐
- `Supplements:` / `Enhances:` - 补充完整性
- **devel 包必须写完整依赖**：`Requires: %{name} = %{version}-%{release}`

---

## ✅ openEuler 检视原则（必须项）

| 检查项 | 说明 |
|--------|------|
| ✅ rpmlint 检查 | 使用 rpmlint 工具检查 |
| ✅ 包命名 | 符合 openEuler 命名规则 |
| ✅ License 字段 | 必须与实际许可证匹配 |
| ✅ spec 文件英语 | 必须用英语撰写且清晰可读 |
| ✅ 源代码匹配 | spec 中 URL 必须与上游源码一致 |
| ✅ ExcludeArch | 未支持的架构必须列出 |
| ✅ 构建依赖完整 | BuildRequires 包含所有依赖 |
| ✅ 处理 locale | 使用 `%find_lang` 宏 |
| ✅ 单一文件不重复 | 原则上不能将单一文件打包到多个 rpm |
| ✅ 文件权限 | 必须正确设置文件权限 |
| ✅ UTF-8 文件名 | rpm 包中的文件名必须是 UTF-8 |

---

## 🔍 常见问题

### Q1: 如何使用 openEuler 专用宏？
见上方 `🔧 openEuler 专用宏` 章节。

### Q2: 如何写 changelog？
见上方 `### 3. changelog 格式` 章节。必须包含标题行（日期+姓名+邮箱+Epoch可选+Version-Release）和内容行（Type/ID/SUG/DESC）。

### Q3: 如何处理多版本包？
openEuler 一般只集成一个版本。如需多版本，需 TC 同意：

```spec
# 使用后缀版本号
Name: mypackage2

# 或描述性后缀
Name: mypackage-stable
```


## 🔄 依赖技能

本技能依赖：

| 技能 | 用途 |
|------|------|
| `rpm` | 基础 RPM 功能（继承所有 rpm 能力） |

---

_版本: 2.0.0 | 作者: openEuler Build Agent_
