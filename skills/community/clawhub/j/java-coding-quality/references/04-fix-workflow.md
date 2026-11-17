# 04 · 门禁分级与修复工作流

本文定义 PMD/SpotBugs 两套原生严重级如何**归并到统一四级**，以及修复-复检循环、误报豁免的操作规范。

## 一、统一严重级映射

两个工具的原生分级不同，统一换算为 **Blocker / Critical / Major / Minor** 四级：

| 统一级 | PMD priority | SpotBugs rank | 门禁要求 |
|---|---|---|---|
| **Blocker** | 1 | 1–4（Scariest） | **必须清零**，否则不通过 |
| **Critical** | 2 | 5–9（Scary） | **必须清零**，否则不通过 |
| **Major** | 3 | 10–14（Troubling） | 尽量修，无法修的登记说明 |
| **Minor** | 4 / 5 | 15–20（Of Concern） | 仅报告，不强制改 |

> 补充规则：**任何 `category='SECURITY'` 的 FindSecBugs 告警，无论 rank，一律至少按 Critical 处理**（安全无小事）；PMD `security` 分类同理。

从报告提取严重级：
- PMD `pmd.xml`：每个 `<violation ... priority='N'>` 的 `priority`。
- SpotBugs `spotbugsXml.xml`：每个 `<BugInstance ... rank='N' category='...'>` 的 `rank` + `category`。

## 二、修复-复检循环

```
1. 编译（被检项目自身 mvn compile——SpotBugs 分析 target/classes，包装工程不编译）
2. 跑 PMD(pmd:pmd) + SpotBugs(spotbugs:spotbugs)，得两份 XML 报告
3. 解析报告 → 按上表归并严重级 → 生成告警清单（按 Blocker→Critical→Major 排序）
4. 从最高级开始逐条修复：
   - 编码手法类 → 查 02/03 速查表
   - 安全类 → 按 03 修复，禁止 suppress
5. 复扫（回到步骤 1）
6. Blocker/Critical 全部清零 → 门禁通过 → 询问是否持久化
```

**修复策略**：
- **同类批量**：同一 bug pattern 命中多处（如多处 `new BigDecimal(double)`），一次性统一改法，改完一起复扫。
- **先高后低**：不要在 Minor 上耗时间；Blocker/Critical 未清零前不处理 Minor。
- **改一类扫一次**：大批量告警时，每修完一个类别就复扫，避免一次改太多引入新问题。

**死循环保护**：同一告警**连续 2 轮**修复仍未消除 → 停下，向用户说明：告警内容、已尝试的两种修法、为何未消除，并申请豁免或请用户决策。**不无限重试**。

## 三、误报判定与豁免

### 3.1 判定标准
- **真阳性**：确实是缺陷/风险 → 修复。
- **误报**：工具因缺乏上下文误判（如框架保证非 null、测试代码、生成代码）→ 才考虑豁免。
- **判定需证据**：说明为什么是误报（数据流事实、框架契约），不能仅因「改起来麻烦」就判误报。

### 3.2 豁免铁律
- 任何豁免**必须经用户确认**，且在代码/配置处**附注释写明理由**。
- **Agent 不得自行豁免安全类告警**（FindSecBugs `SECURITY`、PMD `security`）——只能上报 + 给修复建议，由用户决定。

### 3.3 抑制写法

**PMD**（行级或类级）：
```java
@SuppressWarnings("PMD.AvoidCatchingGenericException") // 理由：框架回调必须捕获所有异常，见 XxxHandler 契约
public void handle() { ... }
```
或用 exclude 文件（`.qualitygate/pmd-exclude.properties`），在包装 pom 配 `<excludeFromFailureFile>`。

**SpotBugs**（需引 `spotbugs-annotations` 依赖）：
```java
@SuppressFBWarnings(value = "EI_EXPOSE_REP", justification = "返回不可变视图，调用方无法修改")
public List<X> getItems() { ... }
```
或用 exclude filter XML（`.qualitygate/spotbugs-exclude.xml`），在包装 pom 配 `<excludeFilterFile>`：
```xml
<Match>
    <Class name="com.example.GeneratedDto"/>
    <Bug pattern="EI_EXPOSE_REP,EI_EXPOSE_REP2"/>
</Match>
```

> 零侵入模式下抑制文件放 `.qualitygate/`；持久化后应随规则集一起纳入版本控制并 code review。

## 四、门禁结论输出

一轮门禁结束后，向用户给出结构化结论：

```
门禁结果：通过 / 未通过
- Blocker：0（已清零）
- Critical：0（已清零）
- Major：N 项（已修 M，登记待议 K）
- Minor：J 项（仅报告，未改）
- 安全类：全部已修复 / 无
- 本轮修复：<清单，含引用的 reference>
- 待用户决策：<误报豁免申请 / 2 轮未消的告警>
```

Blocker/Critical 未清零时，**不得声称门禁通过**；如实报告剩余项与原因。
