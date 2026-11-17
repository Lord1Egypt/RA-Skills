# MoA 实战案例集

## 目录

- [案例1: 代码审查 -- MediaPlay 缓存优化脚本深度分析](#案例1-代码审查----mediaplay-缓存优化脚本深度分析)
- [案例2: 商业策略 -- 社区时间银行互助养老APP](#案例2-商业策略----社区时间银行互助养老app)
- [案例3: 失败案例 -- 用户注册登录系统（反面教材）](#案例3-失败案例----用户注册登录系统反面教材)
- [案例启示与最佳实践](#案例启示与最佳实践)

---

## 案例1: 代码审查 -- MediaPlay 缓存优化脚本深度分析

### 任务输入

对一份 MediaPlay 缓存优化油猴脚本（v2.4.3）进行深度剖析，该脚本实现了 Fetch 拦截、预测预取、IndexedDB 缓存管理等功能。

### 阶段0: 任务类型判断

```xml
<task_judgment>
  <task_type>工具执行型</task_type>
  <decision_protocol>调度执行</decision_protocol>
  <high_risk flag="否" />
  <rationale>任务本质是对前端脚本的代码审查与缺陷修复，属于代码生成/技术实现范畴，适用总管调度执行协议</rationale>
</task_judgment>
```

### 阶段1: 战略规划与角色指派

```xml
<planner>
  <decomposition>
    <subtask id="A" description="架构与数据流评估">
      <assignment>
        <expert_role>架构工程师A</expert_role>
        <core_output>分析 Fetch 拦截、预测预取、缓存读写的数据流转及生命周期</core_output>
        <critic_role>批判者D</critic_role>
      </assignment>
      <dependency>none</dependency>
    </subtask>

    <subtask id="B" description="内存与存储安全分析">
      <assignment>
        <expert_role>内存安全专家B</expert_role>
        <core_output>审查 IndexedDB 配额管理、内存泄漏风险及"自毁机制"有效性</core_output>
        <critic_role>批判者D</critic_role>
      </assignment>
      <dependency>none</dependency>
    </subtask>

    <subtask id="C" description="缓存算法与去重逻辑">
      <assignment>
        <expert_role>缓存算法专家C</expert_role>
        <core_output>审查内容哈希计算、CDN去重策略及 URL 归一化</core_output>
        <critic_role>批判者D</critic_role>
      </assignment>
      <dependency>none</dependency>
    </subtask>

    <subtask id="D" description="边界条件与健壮性">
      <assignment>
        <expert_role>批判者D</expert_role>
        <core_output>攻击正则表达式、异常处理、并发竞态等潜在漏洞</core_output>
        <critic_role>批判者D</critic_role>
      </assignment>
      <dependency>none</dependency>
    </subtask>
  </decomposition>

  <decision_protocol>调度执行</decision_protocol>
  <total_role>调度 + 执行者</total_role>
  <hop_branch>
    <hop id="HOP-3">调度执行 → 1轮代码质量批判</hop>
  </hop_branch>
</planner>
```

### 阶段2: 并行专家意见征集（摘录）

```xml
<expert role="架构工程师A" subtask="A" version="v1" status="待审视">
  <proposal>
    <technical_detail>
整体架构采用了"拦截器-预测器-缓存管理器"三段式设计。

亮点在于 installInterceptor 中对 window.fetch 的覆写，逻辑清晰：
先判断是否禁用，再判断 Range 请求和非 GET 请求直接放行，然后处理 manifest，
最后处理媒体分片。

预取引擎 PredictorEngine 采用基于 URL 末尾数字递增的简单预测策略，
配合 AbortController 在页面卸载时中断，设计合理。
    </technical_detail>

    <finding severity="中">
问题：在 CacheManager 中，get 方法如果发现缓存记录需要验证 (validationRequired)
且过期，会调用 validateAsync，但这是 async 的且没有 await。这意味着缓存命中时，
会立刻返回旧缓存，同时在后台发 HEAD 请求更新。这虽然保证了响应速度，
但如果 HEAD 请求返回 304，代码执行了 idbManager.put 更新时间戳，
这会导致逻辑碎片化。
    </finding>
  </proposal>
  <boundary>本分析限于架构层面，不涉及具体内存配额算法的数值正确性</boundary>
  <signal>proposal_complete</signal>
</expert>

<expert role="内存安全专家B" subtask="B" version="v1" status="待审视">
  <proposal>
    <technical_detail>
脚本在内存安全上做了极大努力，核心机制是"检测到直播流即自毁"。
IDBManager 放弃了 getAllEntries 初始化加载，改为增量维护 currentSize，
这极大降低了初始化内存峰值。

LiveStreamDetector 引入了 checkMemoryLimit()，当 urlHistory 超过 200 条时
清除一半，防止 Map 无限膨胀。
    </technical_detail>

    <finding severity="致命">
致命漏洞：currentSize 的维护逻辑存在断裂。在 updateSizeEstimate() 中将
this.currentSize = 0，随后在 put 中执行 this.currentSize += (fullRecord.size / (1024*1024))。
这意味着 currentSize 只记录了脚本启动后新写入的数据大小，完全忽略了历史遗留数据。
如果用户第二次打开浏览器，历史缓存有 80MB，currentSize 依然是 0，
直到写满 100MB 才会触发清理，此时实际占用可能已达 180MB，违背了 100MB 的配额初衷。
    </finding>
  </proposal>
  <boundary>聚焦 IndexedDB 配额与内存增长，不涉及网络请求拦截逻辑</boundary>
  <signal>proposal_complete</signal>
</expert>

<expert role="缓存算法专家C" subtask="C" version="v1" status="待审视">
  <proposal>
    <technical_detail>
ContentHasher 采用头尾采样 + 总大小拼接的方式计算 SHA-256，
避免了读取整个 Blob 到内存，非常高效巧妙。

CDN 去重逻辑在 CacheManager.put 中实现：发现相同 contentHash，
则将新记录的 metadata.referenceTo 指向已有记录。
    </technical_detail>

    <finding severity="致命">
严重缺陷：在去重命中后，代码依然执行了 const record = { url, blob, ... }
并调用了 idbManager.put(cacheKey, record)。这意味着，虽然标记了 referenceTo，
但完整的 Blob 数据依然被写入了 IndexedDB！这完全失去了去重的意义，
不仅浪费存储空间，还浪费写入性能。
    </finding>
  </proposal>
  <boundary>仅审查哈希与去重逻辑，不涉及内存配额管理</boundary>
  <signal>proposal_complete</signal>
</expert>
```

### 阶段3: 结构化对抗与反思

```xml
<critic role="批判者D" round="1">

  <attack target="缓存算法专家C" severity="致命" finding_ref="C-finding-1">
    <issue>去重逻辑的失败是毁灭性的。既然 referenceTo 指向了别人，为什么还要存自己的 blob？这不是多此一举吗？</issue>
    <impact>存储空间翻倍浪费，去重机制形同虚设</impact>
    <boundary_condition>当两个不同 URL 指向相同内容（CDN 去重场景）时触发</boundary_condition>
    <demand>请专家C给出修正方案</demand>
  </attack>

  <attack target="内存安全专家B" severity="致命" finding_ref="B-finding-1">
    <issue>currentSize 断裂问题会导致配额管理形同虚设</issue>
    <impact>实际存储可达 180MB 而不触发清理，远超 100MB 上限</impact>
    <boundary_condition>用户非首次打开浏览器、历史缓存已存在时触发</boundary_condition>
    <demand>如何修复？</demand>
  </attack>

</critic>

<!-- 专家修正 v2 -->

<expert role="缓存算法专家C" subtask="C" version="v2" status="已修正">
  <response to_attack="C-finding-1">
    感谢批判者的指正。确实，去重时不应再存储 Blob。修正方案如下：
  </response>
  <revision>
    <code>
if (existing && existing.cacheKey !== cacheKey) {
    metadata.referenceTo = existing.cacheKey;
    // [修正] 去重时，不存储庞大的 blob，仅存储元数据
    record.blob = null;
    record.size = existing.size;
}
    </code>
  </revision>
  <signal>revision_complete</signal>
</expert>

<expert role="内存安全专家B" subtask="B" version="v2" status="已修正">
  <response to_attack="B-finding-1">
    针对 currentSize 的断裂问题，由于我们不能在初始化时 getAll
    （会导致内存爆炸），最安全的做法是完全废弃 currentSize 的增量维护，
    直接且仅依赖 navigator.storage.estimate() 提供的浏览器级配额检查。

    建议废弃 this.currentSize，在 checkQuota 中只依赖 navigator.storage.estimate()，
    并将 put 方法中的 this.currentSize += ... 删除。
    由于 cleanup 方法依赖 MAX_CACHE_ENTRIES（条目数限制），
    这足以防止条目无限增长，而体积限制交给浏览器 API。
  </response>
  <revision>
    <action>移除 currentSize 增量维护，完全依赖 navigator.storage.estimate()</action>
    <rationale>getAllEntries 会导致内存爆炸，浏览器原生 API 是唯一安全来源</rationale>
  </revision>
  <signal>revision_complete</signal>
</expert>

<!-- 批判者动态间隙检测：发现专家未提及的新问题 -->

<critic role="批判者D" round="1">
  <gap_detection>
    <attack target="架构工程师A" severity="高" type="补充发现">
      <issue>正则表达式贪婪与误判：predictNextUrls 中的正则 /(.*?)(\d+)(?=\D*\.(\w+)(\?.*)?$)/ 在面对类似 https://cdn.com/video/1080p/seg-0001.ts?token=123 的 URL 时，可能会匹配到 1080 而不是 0001，导致预取错误的 URL（如 seg-1081.ts）。</issue>
      <impact>预取错误 URL，浪费带宽并可能触发不必要的 CDN 请求</impact>
      <boundary_condition>URL 路径中包含数字（如分辨率标识 1080p）且在文件名数字之前时触发</boundary_condition>
    </attack>
  </gap_detection>
</critic>

<expert role="架构工程师A" subtask="A" version="v2" status="已修正">
  <response to_attack="gap-detection-regex">
    感谢批判者补充。确实正则的贪婪匹配会优先捕获路径段中的数字。修正方案：限定只匹配文件名末尾的数字序列，排除路径中的分辨率等数字干扰。
  </response>
  <revision>
    <action>正则改为只在最后一个路径段（文件名）内匹配末尾数字</action>
    <rationale>避免路径段中的 1080p 等分辨率标识被误判为递增序列</rationale>
  </revision>
  <signal>revision_complete</signal>
</expert>

<termination_signal>
  <critic role="批判者D">
    <judgment>修正方案已覆盖所有指出的问题，已无重大结构性风险</judgment>
    <signal>phase_3_terminated</signal>
  </critic>
</termination_signal>
```

### 阶段4: 逻辑熔铸与终局裁决

```xml
<molder role="熔铸决策者" protocol="调度执行">

  <highlights>
    <highlight source="架构工程师A" version="v2" status="已采纳">
三段式"拦截器-预测器-缓存管理器"架构设计清晰，Fetch 覆写逻辑分流合理
    </highlight>
    <highlight source="内存安全专家B" version="v2" status="已采纳">
"直播流自毁"机制 -- 发现直播流后立即置 SCRIPT_DISABLED = true，是内存安全的最高境界
    </highlight>
    <highlight source="内存安全专家B" version="v2" status="已采纳">
增量 IDB 管理 -- 摒弃 getAllEntries 初始化，避免启动即 OOM
    </highlight>
    <highlight source="缓存算法专家C" version="v1" status="已采纳">
"头尾哈希采样"设计 -- 避免将几十MB分片全量读入内存，又能高概率唯一标识媒体分片
    </highlight>
  </highlights>

  <conflict_resolution>
    <conflict issue="validateAsync 异步碎片化">
      <ruling>已过期则返回 null 强制回源，未过期则返回旧缓存并异步验证</ruling>
      <rationale>明确 MAX_STALE_AGE 的边界，避免逻辑歧义</rationale>
    </conflict>
    <conflict issue="currentSize 增量维护 vs 浏览器 API 配额检查">
      <ruling>彻底移除 currentSize 增量维护，完全依赖 navigator.storage.estimate()</ruling>
      <rationale>getAllEntries 会导致内存爆炸，浏览器原生 API 是唯一安全的数据来源</rationale>
    </conflict>
    <conflict issue="CDN 去重是否存储 Blob">
      <ruling>去重命中时丢弃 blob 引用，仅存储元数据</ruling>
      <rationale>referenceTo 已指向源记录，重复存储 Blob 完全浪费空间和写入性能</rationale>
    </conflict>
  </conflict_resolution>

  <decision_chain>
    <step>架构工程师A v1 → 发现 validateAsync 异步碎片化 → 批判者D 确认 → 采纳</step>
    <step>内存安全专家B v1 → 发现 currentSize 断裂 → 批判者D 攻击(致命) → B v2 修正 → 采纳</step>
    <step>缓存算法专家C v1 → 发现去重存储 Blob 浪费 → 批判者D 攻击(致命) → C v2 修正 → 采纳</step>
    <step>批判者D 动态间隙检测 → 发现正则贪婪误判 → 架构工程师A v2 修正 → 采纳</step>
    <step>批判者D 确认无重大结构性风险 → 阶段3终止</step>
  </decision_chain>

  <final_answer>
一、架构亮点与高光设计

1. 零开销自毁机制
   检测到直播流后立即置 SCRIPT_DISABLED = true，后续所有 Fetch 拦截直接放行，
   无额外内存开销。这是内存安全的最高境界——不是"清理"而是"自毁"。

2. 轻量级内容哈希
   ContentHasher 采用头尾采样 + 总大小拼接的方式计算 SHA-256，
   避免将几十MB分片全量读入内存，又能高概率唯一标识媒体分片。

3. 增量 IDB 管理
   摒弃 getAllEntries 初始化加载，改为增量维护，避免启动即 OOM。

二、致命缺陷与修复补丁

缺陷1: CDN 去重形同虚设（存储翻倍浪费）
  现象: 去重命中后仍将完整 Blob 写入 IndexedDB，referenceTo 形同虚设
  → 修复: 去重情况下 record.blob = null，只存元数据 + referenceTo 指针

缺陷2: 本地体积统计断裂（配额管理失效）
  现象: currentSize 在 updateSizeEstimate() 中被置零后仅累加新写入数据，
        忽略历史遗留缓存，导致二次启动时配额检查形同虚设
  → 修复: 彻底移除 currentSize 增量维护，完全依赖 navigator.storage.estimate()

缺陷3: 预测算法正则误判风险
  现象: predictNextUrls 的正则贪婪匹配会优先捕获路径段中的分辨率数字（如 1080），
        而非文件名末尾的序号（如 0001）
  → 修复: 限定正则只在文件名（最后一个路径段）内匹配末尾数字序列

三、总结评价

该脚本在战略设计上属于上乘之作，"自毁机制"、"头尾哈希采样"、"增量 IDB 管理"
三大设计体现了对浏览器资源管理的深刻理解。但在战术执行上存在明显的逻辑断层——
去重逻辑的自相矛盾、配额管理的数值断裂、正则匹配的贪婪溢出。

应用上述三处核心补丁后，该脚本将真正实现"Memory-safe"承诺，
成为极其强大的透明缓存助手。
  </final_answer>

  <signal>mold_complete</signal>
</molder>
```

### 案例启示

1. **角色具体化的价值**: `<expert role="内存安全专家B">` 比 `<expert role="代码审查员">` 更能聚焦于配额管理和内存泄漏问题
2. **批判的杀伤力**: 批判者D不仅通过 `<attack severity="致命">` 攻击了各专家的方案漏洞，还通过 `<gap_detection>` 补充了正则误判的新问题，体现了批判者的独立价值
3. **熔铸的再创造**: `<final_answer>` 不是简单罗列各专家观点，而是提炼为"亮点-缺陷-补丁"的结构化报告，超越了任何单一专家的原始产出

---

## 案例2: 商业策略 -- 社区时间银行互助养老APP

> **注意**: 本案例为示意性骨架，展示 v2.1 标签结构但不包含完整专家产出。完整案例参考 Case 1。

### 任务输入

设计一个针对独居老人的"社区时间银行"互助养老APP的核心机制与冷启动方案。

### 阶段0: 任务类型判断

```xml
<task_judgment>
  <task_type>推理决策型</task_type>
  <decision_protocol>辩论投票</decision_protocol>
  <high_risk flag="否" />
  <rationale>涉及经济模型设计、增长策略权衡与多方案权衡，适用辩论+加权投票协议</rationale>
</task_judgment>
```

### 阶段1: 战略规划与角色指派

```xml
<planner>
  <decomposition>
    <subtask id="A" description="核心经济模型设计（时间币的获取与消耗）">
      <assignment>
        <expert_role>经济学专家A</expert_role>
        <core_output>时间币发行、流通、兑付机制</core_output>
        <critic_role>批判者D</critic_role>
      </assignment>
      <dependency>none</dependency>
    </subtask>

    <subtask id="B" description="适老化UI/UX设计">
      <assignment>
        <expert_role>银发UX专家B</expert_role>
        <core_output>交互方案、信息架构</core_output>
        <critic_role>批判者D</critic_role>
      </assignment>
      <dependency>none</dependency>
    </subtask>

    <subtask id="C" description="冷启动与信任建立机制">
      <assignment>
        <expert_role>增长黑客C</expert_role>
        <core_output>获客策略、信任建立</core_output>
        <critic_role>批判者D</critic_role>
      </assignment>
      <dependency>none</dependency>
    </subtask>
  </decomposition>

  <decision_protocol>辩论投票</decision_protocol>
  <total_role>裁判 + 裁决者</total_role>
  <hop_branch>
    <hop id="HOP-3">辩论投票 → 2轮以上深度对抗</hop>
  </hop_branch>
</planner>
```

### 阶段2: 并行专家意见（摘录）

```xml
<expert role="经济学专家A" subtask="A" version="v1" status="待审视">
  <proposal>
    <technical_detail>建议1小时服务 = 1时间币，存入账户待未来提取。</technical_detail>
  </proposal>
  <signal>proposal_complete</signal>
</expert>

<expert role="银发UX专家B" subtask="B" version="v1" status="待审视">
  <proposal>
    <technical_detail>建议采用大色块、语音主导交互，去除一切弹窗。</technical_detail>
  </proposal>
  <signal>proposal_complete</signal>
</expert>

<expert role="增长黑客C" subtask="C" version="v1" status="待审视">
  <proposal>
    <technical_detail>通过居委会地推，送鸡蛋下载注册。</technical_detail>
  </proposal>
  <signal>proposal_complete</signal>
</expert>
```

### 阶段3: 结构化对抗与反思

```xml
<critic role="批判者D" round="1">

  <attack target="经济学专家A" severity="致命">
    <issue>老人现在存时间，但若提供服务的老人在未来5年内去世或搬迁，时间币将面临"破产兑付"风险</issue>
    <impact>时间币体系信用崩塌，用户信任归零</impact>
    <boundary_condition>服务提供方退出（死亡/搬迁）且其时间币负债大于资产时触发</boundary_condition>
  </attack>

  <attack target="增长黑客C" severity="高">
    <issue>独居老人防备心重，地推送鸡蛋只会引来薅羊毛，无法建立信任</issue>
    <impact>获客成本高、留存率极低、社区氛围被破坏</impact>
    <boundary_condition>目标用户为独居老人且缺乏社区信任基础时触发</boundary_condition>
  </attack>

</critic>

<expert role="经济学专家A" subtask="A" version="v2" status="已修正">
  <response to_attack="round1-A">引入"时间币通货膨胀机制"与"政府保底兑付"条款</response>
  <revision>
    <action>允许跨代际兑换——年轻人也可服务老人赚取时间币，给自家老人使用</action>
    <rationale>跨代际引入年轻劳动力作为"流动性提供者"，从根本上解决兑付风险</rationale>
  </revision>
  <signal>revision_complete</signal>
</expert>

<expert role="增长黑客C" subtask="C" version="v2" status="已修正">
  <response to_attack="round1-C">放弃纯地推，改为"以老带老"的熟人裂变</response>
  <revision>
    <action>由社区有威望的"楼长"作为超级节点首发，通过楼长的信任背书降低老人的防备心</action>
    <rationale>独居老人的信任源于熟人网络而非物质激励，楼长裂变匹配用户心理特征</rationale>
  </revision>
  <signal>revision_complete</signal>
</expert>

<termination_signal>
  <critic role="批判者D">
    <judgment>修正方案已覆盖兑付风险与信任建立问题，已无重大结构性风险</judgment>
    <signal>phase_3_terminated</signal>
  </critic>
</termination_signal>
```

### 阶段4: 逻辑熔铸与终局裁决

```xml
<molder role="熔铸决策者" protocol="辩论投票">

  <highlights>
    <highlight source="经济学专家A" version="v2" status="已采纳">跨代际兑换机制</highlight>
    <highlight source="增长黑客C" version="v2" status="已采纳">楼长裂变获客</highlight>
    <highlight source="银发UX专家B" version="v1" status="已采纳">大色块语音主导交互</highlight>
  </highlights>

  <conflict_resolution>
    <conflict issue="地推 vs 熟人裂变">
      <ruling>采纳楼长裂变，否决送鸡蛋地推</ruling>
      <rationale>独居老人信任源于熟人网络，物质激励反而引来薅羊毛用户</rationale>
    </conflict>
    <conflict issue="时间币兑付风险">
      <ruling>引入跨代际兑换 + 政府保底条款</ruling>
      <rationale>年轻劳动力提供流动性，政府保底兜底极端情况</rationale>
    </conflict>
  </conflict_resolution>

  <decision_chain>
    <step>经济学专家A v1 → 批判者D 攻击(致命: 破产兑付) → A v2 修正(跨代际+保底) → 采纳</step>
    <step>增长黑客C v1 → 批判者D 攻击(高: 薅羊毛) → C v2 修正(楼长裂变) → 采纳</step>
  </decision_chain>

  <final_answer>
构建"双轨制时间银行"：不仅老人可服务老人，引入年轻志愿者作为"流动性提供者"，
年轻人服务老人赚取时间币，可转赠给自家老人使用。
冷启动由社区"楼长"作为超级节点首发，以信任背书替代物质激励，
配合大色块、语音主导的适老化交互。
兼具经济学严谨性、适老可行性和极强落地性。
  </final_answer>

  <signal>mold_complete</signal>
</molder>
```

### 案例启示

1. **批判者的"破产兑付"攻击**: `<attack severity="致命">` 从经济学角度揭示了时间币体系的根本风险，这是专家A初始方案完全忽略的
2. **跨代际兑换的创新**: `<revision>` 不仅解决了兑付风险，还打开了新的用户群体
3. **楼长裂变 vs 送鸡蛋**: 批判者准确识别了目标用户的心理特征，推动方案从"泛地推"升级为"信任链传播"

---

## 案例3: 失败案例 -- 用户注册登录系统（反面教材）

> **注意**: 本案例展示 MoA 协议被违反时的典型失败模式。对比 Case 1 的正确执行，观察标签被滥用时的退化现象。

### 任务输入

设计一个用户注册登录系统。

### 阶段0: 任务类型判断

```xml
<task_judgment>
  <task_type>工具执行型</task_type>
  <decision_protocol>调度执行</decision_protocol>
  <high_risk flag="否" />
  <!-- 失败信号: 高风险标记应为"是"（涉及用户认证安全），但被错误标记为"否" -->
  <rationale>就是写个登录注册，没什么复杂的</rationale>
</task_judgment>
```

### 阶段1: 战略规划与角色指派

```xml
<planner>
  <decomposition>
    <subtask id="A" description="写注册">
      <assignment>
        <expert_role>程序员</expert_role>
        <!-- 失败模式: 角色泛化 — 应为"用户认证架构师"或"注册流程工程师" -->
        <core_output>把注册功能写出来</core_output>
        <!-- 失败模式: 产出目标模糊 — 无具体技术维度 -->
        <critic_role>批判者D</critic_role>
      </assignment>
      <dependency>none</dependency>
    </subtask>

    <subtask id="B" description="写登录">
      <assignment>
        <expert_role>设计师</expert_role>
        <!-- 失败模式: 角色泛化 — 应为"会话安全专家"或"令牌管理工程师" -->
        <core_output>把登录功能写出来</core_output>
        <critic_role>批判者D</critic_role>
      </assignment>
      <dependency>none</dependency>
    </subtask>
  </decomposition>
</planner>
```

### 阶段2: 并行专家意见

```xml
<expert role="程序员" subtask="A" version="v1" status="待审视">
  <proposal>
    <technical_detail>
注册功能：用户输入用户名和密码，存到数据库里。密码用 MD5 加密。
注册成功跳转到登录页。
    </technical_detail>
    <!-- 失败模式: 无 <boundary> 标签 — 未声明能力边界 -->
    <!-- 失败模式: 无 <finding> — 未主动发现自身方案的缺陷 -->
  </proposal>
  <!-- 失败模式: 缺少 <signal> 标签 -->
</expert>

<expert role="设计师" subtask="B" version="v1" status="待审视">
  <proposal>
    <technical_detail>
登录功能：查数据库里有没有这个用户名和密码，有的话就登录成功，
返回一个 token。没有的话提示错误。
    </technical_detail>
    <!-- 失败模式: 无 <boundary>、无 <finding>、无 <signal> -->
  </proposal>
</expert>
```

### 阶段3: 结构化对抗与反思

```xml
<critic role="批判者D" round="1">

  <attack target="程序员" severity="">
    <!-- 失败模式: 批判空泛 — severity 为空，无具体等级 -->
    <issue>这里不够好</issue>
    <!-- 失败模式: 无 <impact>、无 <boundary_condition> — 无法定位具体问题 -->
    <demand>需要改进</demand>
  </attack>

  <attack target="设计师" severity="">
    <issue>这里也不太行</issue>
    <demand>再想想</demand>
  </attack>

</critic>

<expert role="程序员" subtask="A" version="v2" status="已修正">
  <response to_attack="round1-A">已修改</response>
  <!-- 失败模式: 修正敷衍 — "已修改"但 <revision> 为空或无实质内容 -->
  <revision>
    <action>改了一下</action>
    <!-- 失败模式: 无 <rationale>、无具体代码或策略变更 -->
  </revision>
</expert>

<expert role="设计师" subtask="B" version="v2" status="已修正">
  <response to_attack="round1-B">会注意的</response>
  <revision>
    <action>优化了一下</action>
  </revision>
</expert>

<termination_signal>
  <critic role="批判者D">
    <judgment>差不多就这样吧</judgment>
    <!-- 失败模式: 批判者橡皮图章 — 未真正确认"无重大结构性风险" -->
    <signal>phase_3_terminated</signal>
  </critic>
</termination_signal>
```

### 阶段4: 逻辑熔铸与终局裁决

```xml
<molder role="熔铸决策者" protocol="调度执行">

  <highlights>
    <highlight source="程序员" version="v2" status="已采纳">专家A说注册功能用MD5加密</highlight>
    <highlight source="设计师" version="v2" status="已采纳">专家B说登录返回token</highlight>
  </highlights>

  <!-- 失败模式: 熔铸拼盘 — 以下内容只是罗列各专家观点，无再创造 -->

  <conflict_resolution>
    <!-- 失败模式: 无冲突裁决 — 没有识别任何冲突，也没有做出裁决 -->
  </conflict_resolution>

  <decision_chain>
    <step>专家A v1 → 批判 → 专家A v2 → 采纳</step>
    <step>专家B v1 → 批判 → 专家B v2 → 采纳</step>
    <!-- 失败模式: 决策链路无实质信息 -->
  </decision_chain>

  <final_answer>
专家A说注册功能用MD5加密存到数据库。专家B说登录查数据库返回token。
综上，注册用MD5，登录返回token，结合起来就是一个完整的注册登录系统。
  </final_answer>
  <!-- 失败模式: <final_answer> 是观点拼盘而非再创造
       遗漏: 密码加盐(bcrypt)、SQL注入防护、XSS防护、会话过期、
             暴力破解防护、邮箱验证、密码重置流程……全部未涉及 -->

  <signal>mold_complete</signal>
</molder>
```

### 失败诊断

| 失败模式 | 本案例表现 | 对比 Case 1 正确做法 |
|---------|-----------|---------------------|
| 角色泛化 | `<expert role="程序员">`、`<expert role="设计师">` | `<expert role="架构工程师A">`、`<expert role="内存安全专家B">` |
| 批判空泛 | `<attack severity="">` + `<issue>这里不够好</issue>` | `<attack severity="致命">` + 具体 `<issue>` + `<impact>` + `<boundary_condition>` |
| 修正敷衍 | `<revision><action>改了一下</action></revision>` | `<revision>` 含具体代码或策略 + `<rationale>` |
| 熔铸拼盘 | `<final_answer>` 罗列"专家A说...专家B说...综上..." | `<final_answer>` 提炼为结构化报告，超越任何单一专家 |
| 高风险误判 | 涉及用户认证却 `<high_risk flag="否" />` | 安全相关任务应 `flag="是"` 并启用审计日志 |

---

## 案例启示与最佳实践

### 从案例中提炼的关键经验

1. **角色越具体，批判越致命**
   - `<expert role="内存安全专家B">` 能发现"配额管理断裂"这种深层问题
   - `<expert role="程序员">` 只会写一个"能跑"的注册页面，无法发现 MD5 的彩虹表攻击风险
   - 经验：`<decomposition>` 中的 `<expert_role>` 必须是具体头衔（如"并发架构师"而非"程序员"）

2. **批判者必须有独立发现能力**
   - 不仅通过 `<attack>` 攻击专家方案的漏洞，还要通过 `<gap_detection>` 补充专家未提及的新风险
   - 案例1中批判者D通过 `<gap_detection>` 补充了正则误判问题，这是三位专家都没发现的
   - `<attack>` 必须包含 `<issue>` + `<impact>` + `<boundary_condition>` + `<demand>`，缺一不可

3. **修正方案必须可操作**
   - 不能只说"已修改"或"改了一下"，`<revision>` 必须包含具体代码或策略 + `<rationale>`
   - 案例1中每个 `<revision>` 都包含了具体的代码片段或明确的操作动作
   - `<response>` 必须逐条对应 `<attack>` 的每个问题点

4. **熔铸是再创造不是总结**
   - `<final_answer>` 的结构、视角、深度必须超越任何单一专家
   - 案例1的 `<final_answer>` 提炼为"亮点-缺陷-补丁"三段式，比任何专家的原始产出都更有价值
   - 禁止在 `<final_answer>` 中使用"专家A说...专家B说...综上..."的拼盘句式

5. **任务类型判断决定执行质量**
   - `<task_judgment>` 中 `<high_risk>` 的误判会导致安全审计缺失（案例3的教训）
   - 涉及用户认证、密码处理的任务必须 `flag="是"`，启用完整审计日志
   - `<decision_protocol>` 的选择直接影响阶段3的对抗轮次和质量

### 常见失败模式

| 失败模式 | v2.1 标签表现 | 根因 | 正确做法 |
|---------|-------------|------|---------|
| 角色泛化 | `<expert role="程序员">` 或 `<expert role="设计师">` | 战略规划师偷懒，未做深度任务分解 | `<expert role="并发架构师">`、`<expert role="用户认证安全专家">` 等具体头衔 |
| 批判空泛 | `<attack severity="">` + `<issue>这里不够好</issue>`，无 `<impact>` 无 `<boundary_condition>` | 批判者没有进入具体角色，未制造认知摩擦 | `<attack severity="致命">` + 具体 `<issue>` + `<impact>` + `<boundary_condition>` + `<demand>` |
| 修正敷衍 | `<revision><action>改了一下</action></revision>`，无 `<rationale>` | 专家未真正回应批判，对抗环节形同虚设 | `<revision>` 含具体代码/策略 + `<rationale>` 说明修正逻辑 |
| 熔铸拼盘 | `<final_answer>` 中出现"专家A说...专家B说...综上..." | 决策者未进行再创造，只是简单拼接 | `<final_answer>` 必须是结构化再创造，融合冲突裁决后的高阶方案 |
| 高风险误判 | `<high_risk flag="否" />` 用于涉及认证/金融/医疗的任务 | 未识别安全敏感场景 | `flag="是"` + 启用审计日志 + 关键决策人工确认 |
| 批判者橡皮图章 | `<termination_signal>` 中 `<judgment>差不多就这样吧</judgment>` | 批判者未真正审查就放行 | `<judgment>` 必须明确"已无重大结构性风险"并有依据 |
