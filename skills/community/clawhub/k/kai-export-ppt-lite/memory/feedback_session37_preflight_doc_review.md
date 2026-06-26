# Session 37：优化前必须先读文档，避免重复踩坑

## 这轮为什么要专门立规则

最近连续几轮 `data-story` / pill / wrapper / font 优化里，已经出现了同一种低效模式：

1. 某个问题上一轮已经定位清楚
2. 经验也已经写进 `feedback_session*.md`
3. 但下一轮如果不先读文档，还是会按旧假设重新猜一次

这会带来 4 个直接成本：

1. 重复验证已经验证过的根因
2. 重复尝试已经回退过的失败方案
3. 把旧截图/旧 summary 当成新状态，误追 stale compare
4. 忽略“PPTX XML 才是真正写盘结果”这种已经确认的验证口径

## 从本轮起固定下来的优化前流程

每次开始新一轮优化前，必须先做这套 preflight：

1. 读 `docs/设计与实践文档.md`
2. 读 `memory/work-checkpoint.md`
3. 读最近 2-4 份相关 `memory/feedback_session*.md`
4. 用一句 commentary 明确当前已知结论和本轮假设
5. 然后才允许改代码

## 当前必须优先回看的最近记录

### `data-story`

- `feedback_session33_data_story_wrapper_layout.md`
- `feedback_session34_pill_pair_packer.md`
- `feedback_session35_block_pill_component_path.md`
- `feedback_session36_latin_pill_font_mapping.md`

### 验证口径

- stale montage 不能当最新结果
- `python-pptx` 回读对象不能当最终字体真相
- 需要优先核：
  - fresh compare
  - PPTX 实体几何
  - slide XML

## 这条规则的真正目的

不是增加流程负担，而是保证后续每一轮优化都建立在“已知事实”上，而不是建立在模糊记忆上。

对于这个项目，真正耗时的不是改代码，而是：

- 误判根因
- 重复走旧路
- 被旧截图误导

所以从工程效率上，先看文档再优化，反而是更快的路径。
