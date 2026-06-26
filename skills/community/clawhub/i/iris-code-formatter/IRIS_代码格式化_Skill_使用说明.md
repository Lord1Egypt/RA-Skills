[toc]

# IRIS 代码格式化 Skill 使用说明

> **作者**: 姚鑫  
> **邮箱**: 454115408@qq.com  
> **版本**: v3.0

---

## 一、安装方法

### 方式1：通过 WorkBuddy 安装（推荐）

1. 将 `iris-code-formatter` 文件夹复制到 WorkBuddy skills 目录：
   ```
   Windows: C:\Users\<用户名>\.workbuddy\skills\
   ```
   
2. 重启 WorkBuddy 或重新加载技能

### 方式2：通过 OpenClaw/ClawHub 安装

```bash
npx clawhub install iris-code-formatter --workdir <目标路径> --no-input
```

### 方式3：clawhub 下载

- https://clawhub.ai/yaoxin521123/iris-code-formatter



---

## 二、使用方法

### 触发方式

在对话中直接提供 IRIS ObjectScript 代码，Skill 会自动激活并执行代码审查。

**触发关键词：**
- "格式化这段IRIS代码"
- "检查这段代码是否符合规范"
- "审查ObjectScript代码"
- "修正代码风格问题"
- "按照IRIS规范格式化"

### 使用示例

**输入：**
```
Class Util.Encryption.SM3 Extends %RegisteredObject
{
ClassMethod HMAC(key As %Stream.GlobalCharacter, text As %Stream.GlobalCharacter)
{
    s keyStream=..UTF8(key)
    s keyPadding=..KeyPadding(keyStream)
    q ..Str2Hex(hmacByte)
}
...
}
使用iris-code-formatter技能
```

**输出：**

- 修正前代码

![image-20260416165210524](C:\Users\yaoxin521123\AppData\Roaming\Typora\typora-user-images\image-20260416165210524.png)

- 修正后代码

![image-20260416165150802](C:\Users\yaoxin521123\AppData\Roaming\Typora\typora-user-images\image-20260416165150802.png)

---

**以下是输出内容：**



---

---

## 代码审查报告

### 问题汇总

| 类别           | 问题                         | 严重程度 |
| -------------- | ---------------------------- | -------- |
| 方法大括号     | 方法大括号应换行显示         | ⚠️ 警告   |
| 空格规范       | 运算符两侧缺少空格           | ⚠️ 警告   |
| 注释格式       | 方法头注释不规范             | ⚠️ 警告   |
| 变量命名       | 参数命名未使用lowerCamelCase | ⚠️ 警告   |
| 条件后置表达式 | 括号内空格使用错误           | ⚠️ 警告   |
| 字符串拼接     | 单行字段数超过限制           | ⚠️ 警告   |

### 详细问题分析

#### 1. 方法大括号格式问题

**位置**: 所有方法 **问题**: ObjectScript方法大括号应换行显示

```objectscript
// 错误
ClassMethod OrderDetailGrpExecute(...) As %Status {
    s repid=$I(^CacheTemp)
    
// 正确  
ClassMethod OrderDetailGrpExecute(...) As %Status
{
    s repid = $I(^CacheTemp)
```

#### 2. 运算符空格问题

**位置**: 全局 **问题**: `=`、`+`、`-`等运算符左右应加空格

```objectscript
// 错误
s repid=$I(^CacheTemp)
s qHandle=$lb(0,repid,0)
s ind=1

// 正确
s repid = $I(^CacheTemp)
s qHandle = $lb(0, repid, 0)
s ind = 1
```

#### 3. 参数命名问题

**位置**: 所有Query参数**问题**: 参数应使用lowerCamelCase



```objectscript
// 错误
Query OrderDetailGrp(Oeori = "", Oeore = "", DspId = "", ProCode = "")

// 正确
Query OrderDetailGrp(oeori = "", oeore = "", dspId = "", proCode = "")
```

#### 4. 条件后置表达式空格问题

**位置**: OrderDetailGrpExecute, TimeLineExecute等 **问题**: 括号内部条件运算符两侧有空格，但括号与逻辑运算符之间不应有空格

```objectscript
// 错误
i Oeore'="" s Oeori=$p(Oeore,"||",1,2)
e  i DspId'="" s Oeori=$p($g(^DHCOEDISQTY(DspId)),"^",1)
q:Oeori="" $$$OK

// 正确
i (oeore '= "") s oeori = $p(oeore, "||", 1, 2)
e  i (dspId '= "") s oeori = $p($g(^DHCOEDISQTY(dspId)), "^", 1)
q:(oeori = "") $$$OK
```

#### 5. 字符串拼接字段数超限

**位置**: 多处 **问题**: 单行字符串拼接超过5个字段

```objectscript
// 错误
s data = $lb(locDesc, qtyWithUom)

// 建议保持现状（$lb函数本身是内置函数调用）
```

#### 6. 方法头注释不规范

**位置**: 所有方法 **问题**: 缺少规范的docstring注释

```objectscript
// 错误
Query OrderDetailGrp(Oeori = "", ...) As websys.Query(...)

// 正确
/// Desc: 医嘱明细,注意区分门诊住院
/// Output: 两列属性以及值
/// w ##class(%ResultSet).RunQuery("PHA.COM.Query","OrderDetailGrp","41||77")
Query OrderDetailGrp(oeori = "", ...) As websys.Query(...)
```

### 修正后完整代码

以下是按照IRIS代码规范修正后的完整代码：

```
/// Desc: 医嘱明细,注意区分门诊住院
/// Output: 两列属性以及值
/// w ##class(%ResultSet).RunQuery("PHA.COM.Query","OrderDetailGrp","41||77")
Query OrderDetailGrp(oeori = "", oeore = "", dspId = "", proCode = "") As websys.Query(ROWSPEC = "group,field1,value1,field2,value2") [ SqlProc ]
{
}

ClassMethod OrderDetailGrpExecute(ByRef qHandle As %Binary, oeori = "", oeore = "", dspId = "", proCode = "") As %Status
{
    s repid = $I(^CacheTemp)
    s qHandle = $lb(0, repid, 0)
    s ind = 1
    
    #; 处理入参转换
    i (oeore '= "") s oeori = $p(oeore, "||", 1, 2)
    e  i (dspId '= "") s oeori = $p($g(^DHCOEDISQTY(dspId)), "^", 1)
    q:(oeori = "") $$$OK
    
    s ordId = +oeori
    s ordItm = $p(oeori, "||", 2)
    s dspId = $o(^DHCOEDISQTY(0, "OEORI", oeori, ""))
    s admId = $p($g(^OEORD(ordId)), "^", 1)
    q:(admId = "") $$$OK
    s patId = $p(^PAADM(admId), "^", 1)
    s admType = $p(^PAADM(admId), "^", 2)
    s OEORDI1 = $g(^OEORD(ordId, "I", ordItm, 1))
    s OEORDI2 = $g(^OEORD(ordId, "I", ordItm, 2))
    s OEORDI3 = $g(^OEORD(ordId, "I", ordItm, 3))
    s OEORDI5 = $g(^OEORD(ordId, "I", ordItm, 5))
    s OEORDI6 = $g(^OEORD(ordId, "I", ordItm, 6))
    s OEORDI9 = $g(^OEORD(ordId, "I", ordItm, 9))
    s OEORDI11 = $g(^OEORD(ordId, "I", ordItm, 11))
    s OEORDIDHC = $g(^OEORD(ordId, "I", ordItm, "DHC"))
   
...
```

---

---





## 三、规范速查表

### 命名规范

| 类型 | 规则 | 正确示例 | 错误示例 |
|------|------|----------|----------|
| 变量名 | lowerCamelCase | `startDate` | `startdate` |
| 常量 | 全大写 | `MAXCOUNT` | `MaxCount` |
| 布尔变量 | Flag后缀 | `dispFlag` | `isDisp` |
| 方法名 | UpperCamelCase | `GetName()` | `getname()` |
| 布尔方法 | Is开头 | `IsExist()` | `GetExistFlag()` |

### 命令/函数缩写

| 类型 | 全拼 | 缩写 |
|------|------|------|
| 命令 | set/do/quit | s/d/q |
| 命令 | for/while | for/while（全拼） |
| 函数 | $extract/$piece/$length | $e/$p/$l |
| 函数 | $zconvert/$zhex | $zcvt/$zh |

### 格式规范

| 场景 | 正确 | 错误 |
|------|------|------|
| 运算符空格 | `a = b` | `a=b` |
| 后置表达式 | `q:(info = "")` | `q:info=""` |
| 多条件后置 | `q:(a = "")&&(b = "")` | `q:(a = "") && (b = "")` |
| else格式 | `} else {` | `}\nelse {` |

---

## 四、输出说明

### 审查报告结构

```
## 代码审查报告

### 问题汇总
- [严重] 问题1描述（行号）
- [警告] 问题2描述（行号）

### 详细说明
#### 1. 变量命名问题
**位置**：第X行
**问题**：描述
**规范依据**：引用具体规则
**建议修正**：代码示例

### 修正后完整代码
```objectscript
// 完整的修正后代码
```
