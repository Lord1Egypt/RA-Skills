# Skill 写作词汇与进阶判据（定性复核时用）

这套词汇消化自 mattpocock/skills 的 `writing-great-skills`。它给"什么是好 skill"补了一层**可命名的诊断语言**——体检时用这些词点破问题，比泛泛说"太长/有冗余"更准、更可落地。

> 一句话根：**skill 存在是为了从随机系统里榨出确定性。根本美德是「可预测」——每次运行走同一套*过程*（不是产出同一结果）。下面每条判据都为它服务。**

## 一、两种"载荷"——这是"减法"的底层账

- **context load（上下文载荷）**：model-invoked skill 的 `description` 每轮都待在上下文窗口里，是持续成本。正文越长，每次触发付的越多。
- **cognitive load（认知载荷）**：user-invoked skill 不进模型视野，只靠**你**记得它存在——成本转嫁到人脑。
- 当 user-invoked skill 多到记不住，就用一个 **router skill**（一个 user-invoked skill 列出其余的"何时用哪个"）来治认知载荷。

## 二、触发方式：model-invoked vs user-invoked（体检新增维度 #8）

- **model-invoked**（默认，省略 `disable-model-invocation`）：保留 description，模型能自主触发、别的 skill 也能调到它。代价是 context load。
- **user-invoked**（设 `disable-model-invocation: true`）：description 变成给人看的一行摘要，模型够不到，**零 context load**。
- **判据**：这个 skill 是不是**只可能靠人手敲名字**触发？若是 → 该设 user-invoked，别让它的 description 白占每轮上下文。只有"模型必须自己判断何时唤醒"或"别的 skill 要调它"时，才值得付 model-invoked 的常驻成本。

## 三、信息阶梯（progressive disclosure 的标尺）

三级，按"模型多急需"排：① **in-skill step**（SKILL.md 里的有序动作）② **in-skill reference**（按需查的定义/规则，可以是一组平级规则，不是坏味道）③ **external reference**（推到独立文件、靠 context pointer 触发才加载）。

- **branch（分支）= 最干净的拆分测试**：每个分支都要的 → 内联；只有部分分支会走到的 → 推到指针后面。
- **co-location（就近）**：一个概念的定义+规则+注意事项放同一标题下，别散落。
- **context pointer 的措辞**（不是它指向哪）决定模型何时、多可靠地去读那块。

## 四、完成判据（completion criterion）——防"提前收工"

step 类 skill 的每一步要以一个**可检验**的完成条件收尾（模型能分辨"做完了 vs 没做完"）；关键处还要**穷尽**（"每个改过的模型都交代了"，而不是"产出一个变更清单"）。判据含糊 → 招致 **premature completion**（注意力滑向"算完成了"而提前结束）。

## 五、leading word（引导词）

一个模型预训练里已有的**紧凑概念**（如 _tight / red / tracer bullets_），在文里复用，用极少 token 锚定一整片行为。两处获益：正文里锚定**执行**（一见这词就走同一行为），description 里锚定**触发**（你 prompt/文档/代码里都用这词，模型更可靠地联想到该 skill）。把"快、确定、低开销"这种三词重述坍缩成一个 _tight_——既省 token 又给模型更锐的挂钩。体检时主动找"能被一个引导词退休掉的重述"。

## 六、失败模式词汇（诊断用，点名比泛指有力）

- **premature completion**：步骤没真做完就收。先磨锐完成判据（便宜、就地）；判据已无法再细化且确实观察到抢跑，才用"按序列拆分"把后续步骤藏起来。
- **duplication**：同一意思出现在多处。费维护、费 token，还把它在阶梯上的"显要度"抬高过真实等级。守则：每个意思**单一真相源**，改行为只改一处。
- **sediment（沉积）**：旧内容层层留下——"加着安全、删着危险"的默认结局。没有修剪纪律的 skill 必然积沉。
- **sprawl（臃肿）**：纯粹太长，即便每行都还活着且唯一。解药是阶梯：reference 推到指针后、按 branch/序列拆，让每条路径只背自己要的。
- **no-op（空操作）**：模型默认就会做的话，付了载荷却没说事。**测试：这行相对默认行为改变了什么？没有 → 删**。弱引导词（"要认真"而模型本就够认真）就是 no-op，修法是换更强的词（"relentless"），不是换技巧。

## 修剪纪律

逐**句**（不是逐行）跑 no-op 测试：某句在孤立状态下不改变行为 → **整句删掉**，别只删词。要狠——失败的散文多数该删，不是重写。
