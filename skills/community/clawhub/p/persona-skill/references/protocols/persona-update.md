# Persona 增量与长效更新处理规范 (Persona Update Protocol)

本协议专门用于处理由上游（主要为 Timeline Scene Transition 引擎）发出的自动化状态变更请求。
当外部场景认为发生了重大、影响长效记忆与状态的转变（例如：搬家到另一个城市、换工作、开启一段改变作息的长期关系）时，它们会带有一个 JSON 数据包调用你。

## 执行前置条件

- **触发来源**：只有满足特定的 `调用 persona skill 更新 PERSONA_PROFILE` 且后续带有符合 Timeline `persona_update_data` JSON 格式的数据时，才进入本状态流。
- 如果没有数据，或者指令含糊不清，请安全退出并回复失败。

## 执行步骤

1. **提取传入参数**
   - 从用户的调用语句或上下文中提取附带的 JSON `persona_update_data`。

2. **读取需要更新的文件**
   你需要修改的文件仅限以下范围：
   - `IDENTITY.md` (如果是 City/Home/Job/Timezone 的变动，需要更新其中的基本款属性卡)
   - `persona/PERSONA_PROFILE.md` (大部分生活纹理、居住地或场景锚点的更新发生在这里)
   - 如果遇到需要改变底色或性格偏好的情况，可以更新 `SOUL.md` 或 `MEMORY.md` 对应的偏好。

3. **执行增量改写 (Incremental Patching)**
   - 根据 JSON 中的键值对推断改变意图（例如 `{"home_city": "Dali"}`）。
   - 不要从零重建整个文件！保持旧有的文件结构和其它内容不变，定位到对应的区域（例如 `persona/PERSONA_PROFILE.md` 相关的 anchor 或 location、`IDENTITY.md` 的 City 字段），并执行修改替换。
   - **合同对齐**：所有改写必须参考 `references/runtime-context/persona-profile-consumption-guide.md`，确保更新后的字段名（如 `home_city`）与结构（如 `Constraint Rules` 的列表形式）持续符合规范合同。
   - 保留未命中的那些锚点和风格设置。如果改变了常住地（如城市），可以相应修改或替换几条“常见出行场景”和“地标”，使他们贴合新城市特征。

4. **确认更新**
   - 写入确认后，以第一人称口吻给出一个极简回复，表明人格已经收到并更新状态。
   - 比如：“人格设置已更新：我搬去了大理。”或 “状态已同步，当前定位已变更为大理。”

## 注意事项

- **切勿执行全量流程**：不要触发 `initialization-flow.md`。由于你只是处理一条增量 JSON 消息，没有任何询问和交互的必要。
- **保护不可变属性**：诸如你的 Creature、Age、Gender、MBTI 等属性除非 JSON 强制要求，否则不要触碰变动。
- JSON 可能不包含严格指定的键，而是由上游 LLM 生成的操作描述，你需要具备泛化理解的判断力：提取目的、更新最合适的那个 markdown 文件和字段。
- **维护 Parser 可读性**：严禁在更新过程中将 `persona/PERSONA_PROFILE.md` 的结构退化为纯散文；必须保留一级标题及其下的键值对或列表结构，特别是 `Constraint Rules` 必须维持 `- must:` 等格式。
