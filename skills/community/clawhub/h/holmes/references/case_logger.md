# 案件记录方法（命令行参数模式）

**Step 1：查看帮助和格式**
```bash
python3 scripts/holmes_case_logger.py --help
```

**Step 2：按格式填参数**
```bash
python3 scripts/holmes_case_logger.py \
  --problem "问题描述" \
  --model "心智模型" \
  --formula "逻辑公式" \
  --result "结果" \
  --description "结果描述" \
  --time 15 \
  --experiments 1 \
  --switch "切换记录"   # 可选，有则填，无则省略
```

**字段说明**：
| 字段 | 说明 | 必填 |
|------|------|------|
| --problem | 一句话描述解决的问题 | ✅ |
| --model | 心智模型 | ✅ |
| --formula | 逻辑公式（逗号分隔多选） | ✅ |
| --result | 结果：成功 / 失败 / 部分成功 | ✅ |
| --description | **【必填】** 结果描述，三种写法见下方 | ✅ |
| --time | 处理时间（分钟） | ✅ |
| --experiments | 实验次数 | ✅ |
| --switch | 切换记录（有则填，无则省略） | ❌ |

---

## `--description` 写法规范

根据 `--result` 不同，分为三种写法：

### ✅ 成功（为什么成功？采用了什么方法？）
```
--description "成功原因：采用了XX心智模型+XX逻辑公式，溯因链在第X层完整，物理路径可验证...（方法亮点：XXX）"
```

### ❌ 失败（为什么失败？哪些没做到？）
```
--description "失败原因：源于方法还是源于执行？在第X层溯因链断裂；缺失了XX验证/XX步骤；XX步骤跳跃了物理路径..."
```

### 🔄 部分成功（哪部分成功了？为什么？哪部分没做到？为什么？）
```
--description "部分成功：XX部分做到了（采用了XX方法，溯因链完整在XX层）；XX部分没做到（原因是XX，缺失XX步骤/验证）..."
```

---

**心智模型选项**：链条因果 / 排除法 / 反向工程 / 异常锚定 / 主动验证 / 压缩推理 / 阁楼心智

**逻辑公式选项**：排除法 / 选言推理 / 假言推理 / 逆否推理 / 传递公式 / 必要条件 / 矛盾触发 / 因果链 / 或然性推理 / 异常锚定 / 主动验证 / 反向工程 / 归谬法

**触发类型**（填 --switch 时用）：①矛盾 ②推不到结论 ③假设全证伪 ④线索不足 ⑤时间超2倍

**示例（成功，无切换）**：
```bash
python3 scripts/holmes_case_logger.py \
  --problem "系统bug排查" \
  --model "链条因果" \
  --formula "因果链,逆否推理" \
  --result "成功" \
  --description "成功原因：追溯到API调用链路的第三层，找到配置参数写错。采用'链条因果'心智模型+'因果链'公式，逐步验证每个节点，物理路径完整。" \
  --time 5 \
  --experiments 1
```

**示例（失败，无切换）**：
```bash
python3 scripts/holmes_case_logger.py \
  --problem "校园场景推理" \
  --model "异常锚定,链条因果" \
  --formula "排除法,因果链" \
  --result "失败" \
  --description "失败原因：xx方法/执行存在问题，推理深度不足，在第2层就停止了追溯，没有触发网络搜索补充知识。异常点'脸上狰狞笑容'没有作为切入点，而是从'脚步声'方向入手，导致方向错误。" \
  --time 15 \
  --experiments 1
```

**示例（部分成功，有切换）**：
```bash
python3 scripts/holmes_case_logger.py \
  --problem "用户流失分析" \
  --model "排除法" \
  --formula "排除法,或然性推理" \
  --result "部分成功" \
  --description "部分成功：定位到流失节点（注册后第3天），采用了'排除法'过滤了非核心因素；但没有拿到用户行为日志，无法验证'第3天发生了什么'这一关键假设，结果为'可能'而非'确定'。" \
  --time 20 \
  --experiments 2 \
  --switch "线索不足：从行为数据切换到访谈法"
```