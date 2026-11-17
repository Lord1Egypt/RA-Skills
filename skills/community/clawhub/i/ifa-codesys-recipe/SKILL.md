---
name: ifa-codesys-recipe
description: "Manage CODESYS PLC recipes via iFA Evolution �� create, modify, deploy recipe configurations"
tags: [domain-specific, plc, cli, file-based, report-generation]
version: 1.0.0
将汇�?iFA 平台生成的二进制配方文件 (.txtrecipe) 转换�?CoDeSys 风格的纯文本赋值格式，或反向转换�?也支持从 `*.ProdData.txtrecipe` 文件提取凸轮数据，填充到 CoDeSys 文本配方后再转回 iFA 二进制�?
## 两种格式对比

### iFA 二进制格�?(.txtrecipe)
- 文件头部：`recipeName + schemaChecksum_hex(32字节) + varCount(uint32_LE)`
- 数据区：每个变量记录�?`V0_` (0x56 0x30 0x5F) �?`V00_` (0x56 0x30 0x30 0x5F) 标记开�?- 记录结构：`标记 + 变量�?+ 值字节`（紧密排列，无分隔符�?- 值类型由变量名局部段�?IEC 前缀决定
- 文件末尾无终止符

> **V0_ vs V00_**：不同版�?iFA 项目使用不同标记。`ifa_to_codesys.ps1` 自动检测并在输出行前缀中保留（`V0_xxx:=val` �?`V00_xxx:=val`）；`codesys_to_ifa.ps1` 读取该前缀并用正确的字节重建二进制�?
### CoDeSys 文本格式 (.txt)
- 纯文本，每行一个赋值：`V0_变量�?=值` �?`V00_变量�?=值`
- 整数：`20003`、`0`
- 浮点：十进制字符串，�?`481.4893`、`-1391.21`；零值为 `0.0`
- 布尔：`TRUE` / `FALSE`
- 字符串：`''`（单引号�?
## 转换方向

### 方向 A：iFA 二进�?�?CoDeSys 文本

```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>/scripts/ifa_to_codesys.ps1" -SrcDir "<输入目录>" -OutDir "<输出目录>"
```

脚本会：
1. 扫描 SrcDir 下所�?.txtrecipe 文件
2. 自动检�?V0_ / V00_ 标记类型（每文件独立检测）
3. 对每条记录，尝试候选值大�?(1/2/4/8/81)，选取�?IEC 前缀类型自洽的大�?4. 解码值并输出�?`V0_varName:=value` �?`V00_varName:=value` 格式
5. 每个文件生成一�?.txt，另�?00_summary.txt

### 方向 B：CoDeSys 文本 �?iFA 二进�?
```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>/scripts/codesys_to_ifa.ps1" `
    -SrcDir "<输入目录>" `
    -OutDir "<输出目录>" `
    [-ConfigJson "<iFA项目路径>/PLC/<GUID>/RecipeConfig.json"]
```

脚本会：
1. 扫描 SrcDir 下所�?.txt 文件（自动跳�?00_summary.txt�?2. 加载 RecipeConfig.json（优先用 -ConfigJson 参数，否则自动向上查找，最后尝�?PLCSim�?3. 解析每行 `V0_varName:=value` �?`V00_varName:=value` 赋值，自动保留对应的标记字�?4. 根据 IEC 前缀确定值类型；浮点值以十进制字符串解析
5. 编码�?`recipeName + schemaChecksum + count + [标记 + 变量�?+ 值字节]...` 的二进制文件
6. 每个文件生成一�?.txtrecipe

### 方向 C：填充凸轮数据（ProdData �?CoDeSys 文本�?
当用户提�?*填充**�?*填凸�?*�?*把ProdData填入**等，执行以下流程�?
**Step 1**：在当前工作目录（及子目录）查找 `*.ProdData.txtrecipe` 文件�?```powershell
Get-ChildItem "<工作目录>" -Filter "*.ProdData.txtrecipe" -Recurse | Select-Object -First 1
```
若找到多个，列出让用户选择；若找不到，告知用户指定路径�?
**Step 2**：确�?CoDeSys 文本目录（用户已有，或先执行方向 A 生成）�?
**Step 3**：运行填充脚本：
```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>/scripts/fill_cam_data.ps1" `
    -ProdDataFile "<*.ProdData.txtrecipe路径>" `
    -CoDeSysDir   "<CoDeSys文本目录>" `
    -OutDir       "<填充后输出目�?"
```

**Step 4**（可选，用户要求时）：运行方�?B 将填充后�?CoDeSys 文本转回 iFA 二进制�?
## 注意事项

- 输出使用�?BOM �?UTF-8 编码，避免反向转换时首变量名多出 3 字节
- 浮点值使用十进制字符串，存在 ±1 ULP 精度范围（对配方值无实际影响�?- 零值浮点输出为 `0.0`
- 字符串值使用单引号包裹，空字符串为 `''`
- 反向转换时自动处理输入文件可能包含的 UTF-8 BOM
- **校验码必须来�?RecipeConfig.json**；若 iFA 导入�?16385，请确认 -ConfigJson 路径正确
- ProdData 文件�?`astTabData[1, *]`（角度坐标轴，�?0~360）不做填充，只取 `astTabData[2, *]` 的位移数�?
## 脚本位置

所有脚本位于本 skill �?`scripts/` 目录�?- `scripts/ifa_to_codesys.ps1` �?iFA 二进�?�?CoDeSys 文本（自动检�?V0_/V00_ 标记�?- `scripts/codesys_to_ifa.ps1` �?CoDeSys 文本 �?iFA 二进制（保留原始标记类型�?- `scripts/fill_cam_data.ps1`  �?�?*.ProdData.txtrecipe 提取凸轮数据填充�?CoDeSys 文本
