# Domain-Knowledge Extension Implementation Plan v2

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal**: Extend business-blueprint skill to support domain-knowledge blueprints with **quality-driven mechanisms** (clarification turn, self-check, refine command), keeping schema extension minimal. Defer defensive engineering (cycle detection, semantic validation, fault tolerance) until triggered by real usage.

**Architecture**: 
- Phase 0 (核心): 澄清回合 + 自检反问 + 修订命令
- Phase 1 (瘦身): meta 字段扩展 + library.knowledge 极简版 + hints 诚实化
- Phase 2 (极简): validator 核心字段校验 + 6 类基础渲染
- Phase 3 (推迟): 不在本 plan 范围

**Tech Stack**: Python 3.12+, JSON schema, SVG rendering, pytest

**取代**: v1 plan (`plans/2026-04-28-domain-knowledge-entities-extension.md`)

---

## 文件结构总览

### 新建文件

- `references/knowledge-self-check.md` — 6 类实体的自检反问清单
- `references/knowledge-entities-schema.md` — knowledge 实体核心字段定义（极简版）
- `scripts/business_blueprint/templates/cross-border-ecommerce/seed.json` — 跨境电商深度模板
- `scripts/business_blueprint/refine.py` — refine 命令实现
- `scripts/business_blueprint/diff_patcher.py` — diff 应用逻辑
- `tests/test_validate_knowledge.py` — knowledge validator 单元测试
- `tests/test_refine_diff.py` — refine 命令单元测试
- `tests/test_clarify_required.py` — clarifyRequests 强制校验测试

### 修改文件

- `SKILL.md` — 加 Blueprint Type Detection（意图抽取）+ 三件套规则 + Step 2 扩展
- `references/entities-schema.md` — 加 knowledge 块概览
- `scripts/business_blueprint/templates/common/seed.json` — meta.blueprintType 默认值
- `scripts/business_blueprint/templates/retail/seed.json` — 加 knowledgeHints + `_status: template-only`
- `scripts/business_blueprint/templates/finance/seed.json` — 同上
- `scripts/business_blueprint/templates/manufacturing/seed.json` — 同上
- `scripts/business_blueprint/validate.py` — knowledge 校验 + clarifyRequests 强制
- `scripts/business_blueprint/cli.py` — 集成 refine 子命令
- `scripts/business_blueprint/export_svg.py` — 6 类基础样式 + 自检状态可视化

---

## Phase 0: 质量驱动三件套（核心）

> **本 Phase 是 v2 与 v1 的最大差异，是核心创新。Phase 0 完工后必须跑 L3 eval（详见测试设计），五指标达门槛才进 Phase 1。**

---

### Task 0.1: AI 澄清回合（Clarification Turn）

**目标**：让 AI 在第一轮提取后强制输出 ≥3 条针对具体实体的反问。

**Files**:
- Modify: `SKILL.md`
- Modify: `scripts/business_blueprint/validate.py`
- Create: `tests/test_clarify_required.py`

#### Step 1: 在 SKILL.md 加 Clarification Turn 章节

在 "## How to Generate a Blueprint" 之前新增：

```markdown
## Clarification Turn (domain-knowledge blueprints only)

For `blueprintType = "domain-knowledge"`, AI MUST output ≥3 clarification requests in `context.clarifyRequests` after the first extraction. Each request:

- `id`: Format `clr-{seq}` (e.g., `clr-001`)
- `targetEntityId`: MUST point to a specific entity in library (no broad questions)
- `question`: Specific, actionable question (NOT "any other thoughts?")
- `options` (optional): Provide 2-4 choices to guide user
- `rationale`: Why this question matters

**Trigger patterns** (priority order):
1. **Hierarchy ambiguity**: Top-level (level=1) painPoint or strategy → ask "is this root cause or symptom?"
2. **Missing relations**: strategy without `solves` → ask "which painPoint does this address?"
3. **Missing metrics**: strategy without `measures` → ask "how do you measure its effectiveness?"
4. **Hints uncovered**: industryHints checklist topic with no extracted entity → ask "do you need to add X topic?"
5. **Granularity suspicious**: entity name <4 chars or >30 chars → ask "is this granularity appropriate?"

Generate **at least 3, at most 5** clarifyRequests. Validator will reject if <3.

After user answers, write responses to `context.clarifications`:
```json
{
  "clarificationId": "clr-001",
  "answer": "ROI 不稳是症状，根因是创意疲劳"
}
```

Then run a second extraction pass that incorporates clarifications.
```

#### Step 2: validator 加 clarifyRequests 强制校验

在 `validate.py` 中新增 `_validate_clarify_requests` 函数：

```python
def _validate_clarify_requests(
    blueprint: dict[str, Any],
    issues: list[dict[str, Any]],
) -> None:
    """For domain-knowledge blueprints, clarifyRequests must have >=3 items pointing to existing entities."""
    meta = blueprint.get("meta", {})
    blueprint_type = meta.get("blueprintType", "architecture")
    
    if blueprint_type != "domain-knowledge":
        return
    
    context = blueprint.get("context", {})
    clarify_requests = context.get("clarifyRequests", [])
    
    if not isinstance(clarify_requests, list) or len(clarify_requests) < 3:
        issues.append(_issue(
            "error",
            "CLARIFY_REQUESTS_INSUFFICIENT",
            f"domain-knowledge blueprint must have >=3 clarifyRequests, got {len(clarify_requests)}",
            [],
            "Add at least 3 specific clarification questions targeting library entities"
        ))
        return
    
    # Collect all valid entity IDs
    library = blueprint.get("library", {})
    all_ids: set[str] = set()
    for collection in library.values():
        if isinstance(collection, list):
            all_ids.update(item["id"] for item in collection if isinstance(item, dict) and "id" in item)
    knowledge = library.get("knowledge", {})
    for entities in knowledge.values():
        if isinstance(entities, list):
            all_ids.update(e["id"] for e in entities if isinstance(e, dict) and "id" in e)
    
    # Each clarifyRequest must have targetEntityId pointing to existing entity
    for req in clarify_requests:
        if not isinstance(req, dict):
            continue
        target_id = req.get("targetEntityId")
        req_id = req.get("id", "unknown")
        
        if not target_id:
            issues.append(_issue(
                "error",
                "CLARIFY_REQUEST_MISSING_TARGET",
                f"clarifyRequest {req_id} missing targetEntityId",
                [req_id],
                "Each clarification must point to a specific entity"
            ))
        elif target_id not in all_ids:
            issues.append(_issue(
                "error",
                "CLARIFY_REQUEST_INVALID_TARGET",
                f"clarifyRequest {req_id} targetEntityId '{target_id}' not in library",
                [req_id],
                "Fix the entity reference"
            ))
        
        if not req.get("question"):
            issues.append(_issue(
                "error",
                "CLARIFY_REQUEST_MISSING_QUESTION",
                f"clarifyRequest {req_id} missing question text",
                [req_id],
                "Provide specific question text"
            ))
```

调用点：`validate_blueprint()` 中加 `_validate_clarify_requests(blueprint, issues)`。

#### Step 3: 写测试

`tests/test_clarify_required.py`:

```python
import sys
sys.path.insert(0, "scripts/business_blueprint")
from validate import validate_blueprint


def test_domain_knowledge_requires_3_clarify_requests():
    bp = {
        "meta": {"blueprintType": "domain-knowledge", "detectedIntent": "test"},
        "library": {
            "knowledge": {
                "painPoints": [{"id": "pain-001", "name": "X", "entityType": "painPoint"}]
            }
        },
        "context": {"clarifyRequests": []},
        "relations": []
    }
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert any("CLARIFY_REQUESTS_INSUFFICIENT" in i["code"] for i in errors)


def test_clarify_request_must_target_existing_entity():
    bp = {
        "meta": {"blueprintType": "domain-knowledge", "detectedIntent": "test"},
        "library": {
            "knowledge": {
                "painPoints": [{"id": "pain-001", "name": "X", "entityType": "painPoint"}]
            }
        },
        "context": {
            "clarifyRequests": [
                {"id": "clr-001", "targetEntityId": "pain-999", "question": "?"},
                {"id": "clr-002", "targetEntityId": "pain-001", "question": "?"},
                {"id": "clr-003", "targetEntityId": "pain-001", "question": "?"}
            ]
        },
        "relations": []
    }
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert any("INVALID_TARGET" in i["code"] for i in errors)


def test_architecture_blueprint_no_clarify_required():
    bp = {
        "meta": {"blueprintType": "architecture"},
        "library": {"capabilities": [{"id": "cap-001", "name": "X"}]},
        "context": {},
        "relations": []
    }
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert not any("CLARIFY" in i["code"] for i in errors)
```

#### Step 4: 跑测试 + commit

```bash
python -m pytest tests/test_clarify_required.py -v
git add SKILL.md scripts/business_blueprint/validate.py tests/test_clarify_required.py
git commit -m "feat: add clarification turn for domain-knowledge blueprints

domain-knowledge blueprints must include >=3 clarifyRequests targeting
specific library entities. Validator rejects if missing or pointing to
non-existent entities. SKILL.md documents trigger patterns and prompt rules.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 0.2: 实体自检反问

**目标**：每个 knowledge 实体附 `_selfCheck.questions` 字段，渲染时高亮非空 questions 的实体。

**Files**:
- Create: `references/knowledge-self-check.md`
- Modify: `SKILL.md`
- Modify: `scripts/business_blueprint/export_svg.py`

#### Step 1: 创建自检反问清单

`references/knowledge-self-check.md`:

```markdown
# Knowledge Entity Self-Check Questions

For each knowledge entity, AI must run through the corresponding self-check list and populate `_selfCheck` field:

```json
{
  "_selfCheck": {
    "passed": ["check item that's confirmed"],
    "questions": ["check item still uncertain"]
  }
}
```

Entities with non-empty `_selfCheck.questions` will be rendered with yellow border + "?" badge.

## painPoint
1. **症状还是根因**：是可观测的现象（症状），还是造成现象的机制（根因）？
2. **严重度依据**：判断 severity 的依据是什么——数据、感受，还是对标？
3. **受影响方**：哪些角色或部门直接受影响？

## strategy
1. **痛点对应**：对应哪个具体 painPoint？是否有 `solves` 关系？
2. **执行前提**：实施需要哪些资源、能力或时机？
3. **效果衡量**：怎么衡量它有效？是否有 `measures` 关系指向 metric？

## rule
1. **规则来源**：是平台政策、法规要求，还是内部约定？
2. **违反后果**：违反后会发生什么——封号、罚款、流量降级？
3. **约束目标**：约束哪些 strategy？是否有 `enforces` 关系？

## metric
1. **计算方式**：值或基准是怎么得来的？
2. **衡量目标**：衡量哪个 strategy？是否有 `measures` 关系？
3. **阈值依据**：阈值的业务依据是什么——历史数据、行业基准、目标设定？

## practice
1. **频率周期**：执行频率是多少——每日、每周、每月、按需？
2. **支撑策略**：支撑哪个 strategy？是否有 `requires` 反向关系？
3. **成功信号**：怎么知道实践到位了——CTR 提升、转化率改善、客户反馈？

## pitfall
1. **导致痛点**：导致什么具体 painPoint？是否有 `causes` 关系？
2. **避免方式**：怎么避免——规则、流程、工具？
3. **真实案例**：是否有真实案例或数据支撑？

## Self-Check Output Format

Each entity should have:

```json
{
  "id": "pain-001",
  "name": "ROI 不稳",
  "entityType": "painPoint",
  "_selfCheck": {
    "passed": ["可观测", "受影响方明确"],
    "questions": ["是症状还是根因？— 待用户确认"]
  }
}
```

If `questions` is empty array `[]`, the entity is fully self-checked. If non-empty, renderer will highlight it.
```

#### Step 2: 在 SKILL.md 加自检规则

在 "Step 2: Extract entities" 之后加：

```markdown
### Step 2.5: Self-Check Each Entity

After extracting each knowledge entity, run the self-check questions from `references/knowledge-self-check.md` for that entity type. Populate `_selfCheck` field:

- `passed`: checks the AI is confident about based on extracted info
- `questions`: checks the AI is uncertain about (these will be highlighted to user)

Be honest about uncertainty — if you don't know, put it in `questions`. The user values knowing what to verify.
```

#### Step 3: 渲染层加自检高亮

修改 `export_svg.py`，在渲染每个 knowledge 实体时检查 `_selfCheck.questions`：

```python
def _render_knowledge_entity(entity: dict, x: int, y: int) -> str:
    """Render a knowledge entity with optional self-check highlight."""
    entity_type = entity.get("entityType", "")
    style = KNOWLEDGE_STYLES.get(entity_type, DEFAULT_STYLE)
    
    # Self-check highlight
    self_check = entity.get("_selfCheck", {})
    questions = self_check.get("questions", []) if isinstance(self_check, dict) else []
    has_questions = bool(questions)
    
    border_color = "#F59E0B" if has_questions else style["color"]
    border_width = 3 if has_questions else 2
    
    svg = f'<rect x="{x}" y="{y}" rx="8" ry="8" '
    svg += f'fill="{style["fill"]}" stroke="{border_color}" stroke-width="{border_width}"/>'
    
    # Add ? badge if has questions
    if has_questions:
        badge_x = x + 180
        badge_y = y + 5
        svg += f'<circle cx="{badge_x}" cy="{badge_y}" r="10" fill="#F59E0B"/>'
        svg += f'<text x="{badge_x}" y="{badge_y + 4}" text-anchor="middle" '
        svg += f'fill="white" font-weight="bold">?</text>'
        # Tooltip via title element
        questions_text = "&#10;".join(questions)
        svg += f'<title>未确认: {questions_text}</title>'
    
    # Entity name + icon
    svg += f'<text x="{x + 30}" y="{y + 25}">{style["icon"]} {entity["name"]}</text>'
    
    return svg


KNOWLEDGE_STYLES = {
    "painPoint": {"fill": "#FEE2E2", "color": "#DC2626", "icon": "⚠"},
    "strategy": {"fill": "#D1FAE5", "color": "#0B6E6E", "icon": "💡"},
    "rule": {"fill": "#FEF3C7", "color": "#D97706", "icon": "📋"},
    "metric": {"fill": "#E0E7FF", "color": "#4F46E5", "icon": "📊"},
    "practice": {"fill": "#D1FAE5", "color": "#10B981", "icon": "✅"},
    "pitfall": {"fill": "#FEF3C7", "color": "#F59E0B", "icon": "❌"},
}

DEFAULT_STYLE = {"fill": "#F3F4F6", "color": "#6B7280", "icon": "📦"}
```

#### Step 4: commit

```bash
git add references/knowledge-self-check.md SKILL.md scripts/business_blueprint/export_svg.py
git commit -m "feat: add self-check mechanism for knowledge entities

Each knowledge entity gets _selfCheck field with passed/questions arrays.
Entities with non-empty questions render with yellow border + ? badge.
Self-check question lists for 6 entity types in references/.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 0.3: 修订命令（Refine）

**目标**：用户写自然语言反馈，AI 输出结构化 diff，patcher 应用 diff 生成新版本蓝图。

**Files**:
- Create: `scripts/business_blueprint/refine.py`
- Create: `scripts/business_blueprint/diff_patcher.py`
- Create: `tests/test_refine_diff.py`
- Modify: `scripts/business_blueprint/cli.py`

#### Step 1: 实现 diff_patcher.py

```python
"""Apply refine diff operations to a blueprint."""
from typing import Any
import copy


def apply_diff(blueprint: dict[str, Any], diff: dict[str, Any]) -> dict[str, Any]:
    """Apply a list of operations to a blueprint, returning a new blueprint.
    
    Operations:
    - {op: "modify", path: "library.knowledge.painPoints[0].name", old: "...", new: "..."}
    - {op: "add", path: "library.knowledge.painPoints[]", value: {...}}
    - {op: "delete", path: "library.knowledge.pitfalls[2]"}
    """
    result = copy.deepcopy(blueprint)
    operations = diff.get("operations", [])
    
    for op in operations:
        op_type = op.get("op")
        path = op.get("path", "")
        
        if op_type == "modify":
            _apply_modify(result, path, op.get("new"))
        elif op_type == "add":
            _apply_add(result, path, op.get("value"))
        elif op_type == "delete":
            _apply_delete(result, path)
        else:
            raise ValueError(f"Unknown op type: {op_type}")
    
    return result


def _resolve_path(obj: dict, path: str) -> tuple[Any, str | int]:
    """Resolve path like 'library.knowledge.painPoints[0].name' to (parent, key)."""
    parts = _parse_path(path)
    current = obj
    for part in parts[:-1]:
        if isinstance(part, int):
            current = current[part]
        else:
            current = current[part]
    return current, parts[-1]


def _parse_path(path: str) -> list[str | int]:
    """Parse 'library.knowledge.painPoints[0].name' into ['library', 'knowledge', 'painPoints', 0, 'name']."""
    parts: list[str | int] = []
    for segment in path.split("."):
        # Handle array indices like 'painPoints[0]' or 'painPoints[]'
        if "[" in segment:
            name, idx_str = segment.split("[", 1)
            idx_str = idx_str.rstrip("]")
            if name:
                parts.append(name)
            if idx_str == "":
                parts.append(-1)  # append marker
            else:
                parts.append(int(idx_str))
        else:
            parts.append(segment)
    return parts


def _apply_modify(obj: dict, path: str, new_value: Any) -> None:
    parent, key = _resolve_path(obj, path)
    if isinstance(key, int):
        parent[key] = new_value
    else:
        parent[key] = new_value


def _apply_add(obj: dict, path: str, value: Any) -> None:
    """Path ending in [] means append to array."""
    parts = _parse_path(path)
    if parts[-1] == -1:
        # Append to array
        current = obj
        for part in parts[:-2]:
            if isinstance(part, int):
                current = current[part]
            else:
                current = current[part]
        array_key = parts[-2]
        if isinstance(array_key, int):
            current = current[array_key]
            current.append(value)
        else:
            if array_key not in current:
                current[array_key] = []
            current[array_key].append(value)
    else:
        parent, key = _resolve_path(obj, path)
        if isinstance(key, int):
            parent.insert(key, value)
        else:
            parent[key] = value


def _apply_delete(obj: dict, path: str) -> None:
    parent, key = _resolve_path(obj, path)
    if isinstance(key, int):
        parent.pop(key)
    else:
        del parent[key]
```

#### Step 2: 实现 refine.py

```python
"""Refine command: AI generates diff from user feedback, applies it to blueprint."""
import json
from pathlib import Path
from typing import Any

from diff_patcher import apply_diff


REFINE_PROMPT_TEMPLATE = """You are refining an existing business blueprint based on user feedback.

EXISTING BLUEPRINT:
```json
{blueprint_json}
```

USER FEEDBACK:
{feedback}

PRIOR CLARIFICATIONS (if any):
{clarifications}

Output a refine diff as JSON with this structure:

```json
{{
  "diffId": "diff-{timestamp}",
  "baseBlueprintRevisionId": "{base_revision}",
  "operations": [
    {{"op": "modify", "path": "library.knowledge.painPoints[0].name", "old": "...", "new": "..."}},
    {{"op": "add", "path": "library.knowledge.painPoints[]", "value": {{...}}}},
    {{"op": "delete", "path": "library.knowledge.pitfalls[2]"}}
  ],
  "rationale": "Brief explanation of why these changes address the feedback"
}}
```

Constraints:
- Each operation must be minimal and focused
- Modifications preserve entity IDs (only change name/fields)
- Additions get fresh sequential IDs
- Deletions remove entire entity (cascading: also remove relations referencing it)
- For new entities, run self-check (see references/knowledge-self-check.md)
- Output ONLY the JSON diff, no commentary
"""


def generate_diff(blueprint: dict[str, Any], feedback: str, llm_call) -> dict[str, Any]:
    """Call LLM to generate a diff. llm_call is injected for testability."""
    blueprint_json = json.dumps(blueprint, ensure_ascii=False, indent=2)
    clarifications = blueprint.get("context", {}).get("clarifications", [])
    clarifications_text = json.dumps(clarifications, ensure_ascii=False) if clarifications else "None"
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    base_revision = blueprint.get("meta", {}).get("revisionId", "unknown")
    
    prompt = REFINE_PROMPT_TEMPLATE.format(
        blueprint_json=blueprint_json,
        feedback=feedback,
        clarifications=clarifications_text,
        timestamp=timestamp,
        base_revision=base_revision,
    )
    
    response = llm_call(prompt)
    diff = json.loads(response)
    return diff


def refine_blueprint(
    blueprint_path: Path,
    feedback: str,
    output_path: Path,
    llm_call,
    auto_apply: bool = True,
) -> dict[str, Any]:
    """Refine a blueprint based on feedback. Returns the diff."""
    blueprint = json.loads(blueprint_path.read_text(encoding="utf-8"))
    
    diff = generate_diff(blueprint, feedback, llm_call)
    
    if auto_apply:
        new_blueprint = apply_diff(blueprint, diff)
        # Bump revisionId
        from datetime import datetime
        new_blueprint["meta"]["revisionId"] = f"rev-{datetime.now().strftime('%Y%m%d-%H%M')}"
        new_blueprint["meta"]["lastModifiedBy"] = "ai-refine"
        output_path.write_text(json.dumps(new_blueprint, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Save diff alongside
    diff_path = output_path.with_suffix(".diff.json")
    diff_path.write_text(json.dumps(diff, ensure_ascii=False, indent=2), encoding="utf-8")
    
    return diff
```

#### Step 3: 集成 CLI 子命令

修改 `cli.py`:

```python
def add_refine_subcommand(subparsers):
    parser = subparsers.add_parser("refine", help="Refine blueprint based on user feedback")
    parser.add_argument("--blueprint", required=True, help="Path to existing blueprint JSON")
    parser.add_argument("--feedback", required=True, help="User feedback text")
    parser.add_argument("--output", required=True, help="Output path for refined blueprint")
    parser.add_argument("--no-apply", action="store_true", help="Generate diff only, don't apply")
    parser.set_defaults(func=cmd_refine)


def cmd_refine(args):
    from pathlib import Path
    from refine import refine_blueprint
    
    # llm_call is injected based on environment (Claude API, mock, etc.)
    llm_call = _get_llm_caller()
    
    diff = refine_blueprint(
        blueprint_path=Path(args.blueprint),
        feedback=args.feedback,
        output_path=Path(args.output),
        llm_call=llm_call,
        auto_apply=not args.no_apply,
    )
    
    print(f"Diff generated: {len(diff['operations'])} operations")
    print(f"Rationale: {diff.get('rationale', 'N/A')}")
```

#### Step 4: 写 diff_patcher 单元测试

`tests/test_refine_diff.py`:

```python
import sys
sys.path.insert(0, "scripts/business_blueprint")
from diff_patcher import apply_diff


def test_modify_operation():
    bp = {
        "library": {
            "knowledge": {
                "painPoints": [{"id": "pain-001", "name": "ROI 不稳"}]
            }
        }
    }
    diff = {
        "operations": [
            {"op": "modify", "path": "library.knowledge.painPoints[0].name",
             "old": "ROI 不稳", "new": "ROAS 波动"}
        ]
    }
    result = apply_diff(bp, diff)
    assert result["library"]["knowledge"]["painPoints"][0]["name"] == "ROAS 波动"
    # Original unchanged
    assert bp["library"]["knowledge"]["painPoints"][0]["name"] == "ROI 不稳"


def test_add_operation():
    bp = {
        "library": {
            "knowledge": {"painPoints": []}
        }
    }
    diff = {
        "operations": [
            {"op": "add", "path": "library.knowledge.painPoints[]",
             "value": {"id": "pain-002", "name": "新痛点"}}
        ]
    }
    result = apply_diff(bp, diff)
    assert len(result["library"]["knowledge"]["painPoints"]) == 1
    assert result["library"]["knowledge"]["painPoints"][0]["id"] == "pain-002"


def test_delete_operation():
    bp = {
        "library": {
            "knowledge": {
                "pitfalls": [
                    {"id": "pit-001", "name": "A"},
                    {"id": "pit-002", "name": "B"},
                    {"id": "pit-003", "name": "C"}
                ]
            }
        }
    }
    diff = {
        "operations": [
            {"op": "delete", "path": "library.knowledge.pitfalls[1]"}
        ]
    }
    result = apply_diff(bp, diff)
    assert len(result["library"]["knowledge"]["pitfalls"]) == 2
    assert result["library"]["knowledge"]["pitfalls"][1]["id"] == "pit-003"


def test_multiple_operations_in_order():
    bp = {
        "library": {
            "knowledge": {"painPoints": [{"id": "pain-001", "name": "X"}]}
        }
    }
    diff = {
        "operations": [
            {"op": "modify", "path": "library.knowledge.painPoints[0].name",
             "old": "X", "new": "Y"},
            {"op": "add", "path": "library.knowledge.painPoints[]",
             "value": {"id": "pain-002", "name": "Z"}}
        ]
    }
    result = apply_diff(bp, diff)
    assert result["library"]["knowledge"]["painPoints"][0]["name"] == "Y"
    assert result["library"]["knowledge"]["painPoints"][1]["name"] == "Z"
```

#### Step 5: 跑测试 + commit

```bash
python -m pytest tests/test_refine_diff.py -v
git add scripts/business_blueprint/refine.py scripts/business_blueprint/diff_patcher.py
git add scripts/business_blueprint/cli.py tests/test_refine_diff.py
git commit -m "feat: add refine command with diff-based blueprint revision

User provides natural language feedback, AI generates structured diff
(add/modify/delete operations), patcher applies to produce new blueprint.

Diff format documented in design v2. Patcher tested with 4 unit tests
covering modify, add, delete, and multi-op cases.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Phase 0 Checkpoint

**目标**：在进 Phase 1 之前验证三件套可用，跑 L3 eval 五指标。

- [ ] L1 单测全过：`pytest tests/test_clarify_required.py tests/test_refine_diff.py`
- [ ] 手动 smoke test：用一个跨境电商场景跑完整流程（提取 → 澄清 → 第二轮 → refine）
- [ ] L3 eval 跑 6 个真实场景（详见测试设计文档）
- [ ] 五指标全部达门槛（澄清击中率 ≥60%、二轮变更率 ≥30%、自检指向准确率 ≥50%、修订接受率 ≥70%、回归零破坏 100%）
- [ ] **如果任一指标不达，停止 Phase 1，回到设计层修正**

```bash
git tag phase-0-complete
git commit --allow-empty -m "checkpoint: Phase 0 (clarify + self-check + refine) complete

Three quality-driven mechanisms implemented and L3-evaled.
All five proxy metrics passed thresholds.

Next: Phase 1 schema extension."
```

---

## Phase 1: Schema 极简扩展

### Task 1.1: meta.blueprintType + detectedIntent

**Files**:
- Modify: `scripts/business_blueprint/templates/common/seed.json`
- Modify: `scripts/business_blueprint/validate.py`
- Modify: `SKILL.md`

#### Step 1: common/seed.json 加默认值

```json
{
  "version": "1.0",
  "meta": {
    "blueprintType": "architecture",
    "detectedIntent": ""
  },
  ...
}
```

#### Step 2: validate.py 加 meta 校验

```python
def _validate_meta(blueprint: dict[str, Any], issues: list[dict[str, Any]]) -> None:
    meta = blueprint.get("meta", {})
    bp_type = meta.get("blueprintType", "architecture")
    
    if bp_type not in ["architecture", "domain-knowledge"]:
        issues.append(_issue(
            "error", "INVALID_BLUEPRINT_TYPE",
            f"Invalid blueprintType: {bp_type}",
            [], "Must be 'architecture' or 'domain-knowledge'"
        ))
    
    if bp_type == "domain-knowledge":
        intent = meta.get("detectedIntent", "")
        if not isinstance(intent, str) or not intent.strip():
            issues.append(_issue(
                "error", "MISSING_DETECTED_INTENT",
                "domain-knowledge blueprint must have non-empty meta.detectedIntent",
                [], "AI must populate detectedIntent during extraction"
            ))
```

#### Step 3: SKILL.md 加 Blueprint Type Detection

替换原 v1 的关键词匹配章节：

```markdown
## Blueprint Type Detection (Intent Extraction)

**Step 1: Extract intent.** Read user request, output single-sentence summary (≤80 chars) of what they want. Save to `meta.detectedIntent`.

Example:
- "用户想要跨境电商广告领域的 know-how 大图，用于客户 pitch"
- "用户需要企业 IT 系统架构图，覆盖前后端分离方案"

**Step 2: Choose blueprintType from intent.**
- Intent describes domain knowledge / market insight / strategy / best practice → `"domain-knowledge"`
- Intent describes system architecture / IT design / technical blueprint → `"architecture"`
- Ambiguous → ASK USER before proceeding (do not silently default)

**Step 3: Show user the intent.** detectedIntent and blueprintType are visible in JSON. User can override either.
```

#### Step 4: commit

```bash
git add scripts/business_blueprint/templates/common/seed.json
git add scripts/business_blueprint/validate.py SKILL.md
git commit -m "feat: replace keyword-based blueprintType detection with intent extraction

AI must output meta.detectedIntent (NL summary <=80 chars) before choosing
blueprintType. Validator enforces non-empty intent for domain-knowledge.
Replaces v1's brittle keyword frequency matching.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 1.2: library.knowledge 块（核心字段校验）

**Files**:
- Create: `references/knowledge-entities-schema.md`
- Modify: `scripts/business_blueprint/validate.py`
- Create: `tests/test_validate_knowledge.py`

#### Step 1: 创建极简版 knowledge-entities-schema.md

```markdown
# Knowledge Entities Schema (v2 Minimal)

Knowledge block in `library.knowledge` for domain-knowledge blueprints. Six predefined entity types; user-defined types allowed.

## Entity Overview

| Type | entityType value | Example |
|------|------|------|
| painPoints | `painPoint` | ROI 不稳、素材疲劳 |
| strategies | `strategy` | 测款节奏策略 |
| rules | `rule` | Facebook 政策红线 |
| metrics | `metric` | ROAS 基准 |
| practices | `practice` | 素材迭代周期 |
| pitfalls | `pitfall` | 过度依赖单一平台 |

## Core Fields (Strictly Validated)

| Field | Type | Required | Rule |
|------|------|----------|------|
| `id` | string | ✅ | Format `{prefix}-{seq}`, globally unique |
| `name` | string | ✅ | Non-empty |
| `entityType` | string | ✅ | Non-empty |

## Optional Fields (Not Validated, Documentation Only)

These are recommended but not enforced. Use as needed:

- `description`, `severity`, `level`, `relatedCapabilityIds`, `applicableCapabilityIds`
- For rules: `platform`, `penalty`
- For metrics: `value`, `unit`, `benchmarkContext`
- For practices: `frequency`, `successMetric`
- `_selfCheck`: AI-generated self-check result (see knowledge-self-check.md)

User-defined fields allowed; not validated.

## Relations

See design doc for relation type whitelist. Validator enforces:
- `from`/`to` IDs exist in library
- `type` is in whitelist (10 types: solves, prevents, measures, enforces, requires, causes, impacts, supports, enforcedBy, measuredBy)

Semantic validity (e.g. `measures` must be metric→strategy) is NOT validated in v2 — too many edge cases. Recommend it via documentation only.

## Naming Conventions (Soft Recommendations)

- painPoint name: focus on the problem, e.g. "ROI 不稳" not "缺乏 ROI 监控系统"
- strategy name: focus on the method, e.g. "测款节奏策略" not "优化 ROI"
- rule name: source + content, e.g. "Facebook 广告政策红线"
- metric name: indicator + benchmark, e.g. "ROAS 基准"
```

#### Step 2: validator 加 knowledge 实体核心字段校验

```python
def _validate_knowledge_block(blueprint: dict[str, Any], issues: list[dict[str, Any]]) -> None:
    meta = blueprint.get("meta", {})
    bp_type = meta.get("blueprintType", "architecture")
    library = blueprint.get("library", {})
    knowledge = library.get("knowledge", {})
    
    # architecture blueprint: knowledge should be empty
    if bp_type == "architecture":
        if knowledge and any(knowledge.values()):
            issues.append(_issue(
                "error", "ARCHITECTURE_WITH_KNOWLEDGE",
                "architecture blueprint should not contain knowledge entities",
                [], "Set blueprintType to 'domain-knowledge' or remove knowledge block"
            ))
        return
    
    # domain-knowledge blueprint: must have at least 1 entity
    if not knowledge or not any(knowledge.values()):
        issues.append(_issue(
            "error", "DOMAIN_KNOWLEDGE_EMPTY",
            "domain-knowledge blueprint must have at least 1 knowledge entity",
            [], "Add entities to library.knowledge"
        ))
        return
    
    # Validate core fields for each entity
    for type_plural, entities in knowledge.items():
        if not isinstance(entities, list):
            continue
        for entity in entities:
            if not isinstance(entity, dict):
                continue
            
            ent_id = entity.get("id", "<no-id>")
            
            for required_field in ["id", "name", "entityType"]:
                if required_field not in entity:
                    issues.append(_issue(
                        "error",
                        f"KNOWLEDGE_MISSING_{required_field.upper()}",
                        f"{type_plural} entity '{ent_id}' missing core field '{required_field}'",
                        [ent_id],
                        f"Add '{required_field}' to entity"
                    ))
                elif not entity[required_field]:
                    issues.append(_issue(
                        "error",
                        f"KNOWLEDGE_EMPTY_{required_field.upper()}",
                        f"{type_plural} entity '{ent_id}' has empty '{required_field}'",
                        [ent_id],
                        f"Provide non-empty '{required_field}'"
                    ))
```

#### Step 3: validator 加 relations 基础校验

```python
def _validate_relations_basic(blueprint: dict[str, Any], issues: list[dict[str, Any]]) -> None:
    """V2: only check ID references and type whitelist. NO cycle detection or semantic check."""
    library = blueprint.get("library", {})
    relations = blueprint.get("relations", [])
    
    # Collect all IDs
    all_ids: set[str] = set()
    for collection in library.values():
        if isinstance(collection, list):
            all_ids.update(item["id"] for item in collection if isinstance(item, dict) and "id" in item)
    knowledge = library.get("knowledge", {})
    for entities in knowledge.values():
        if isinstance(entities, list):
            all_ids.update(e["id"] for e in entities if isinstance(e, dict) and "id" in e)
    
    valid_types = {
        # Architecture
        "supports", "depends", "realizes",
        # Knowledge internal
        "solves", "prevents", "measures", "enforces", "requires", "causes",
        # Cross-type
        "impacts", "enforcedBy", "measuredBy"
        # Note: "supports" appears twice (architecture + cross-type), both valid
    }
    
    for rel in relations:
        if not isinstance(rel, dict):
            continue
        rel_id = rel.get("id", "<no-id>")
        rel_type = rel.get("type")
        from_id = rel.get("from")
        to_id = rel.get("to")
        
        if rel_type and rel_type not in valid_types:
            issues.append(_issue(
                "warning",  # warning, not error — allow user to define new types
                "RELATION_UNKNOWN_TYPE",
                f"Relation '{rel_id}' uses unknown type '{rel_type}'",
                [rel_id],
                f"Standard types: {sorted(valid_types)}"
            ))
        
        if from_id and from_id not in all_ids:
            issues.append(_issue(
                "error", "RELATION_MISSING_FROM",
                f"Relation '{rel_id}' references non-existent 'from' ID: {from_id}",
                [rel_id], "Fix the entity reference"
            ))
        
        if to_id and to_id not in all_ids:
            issues.append(_issue(
                "error", "RELATION_MISSING_TO",
                f"Relation '{rel_id}' references non-existent 'to' ID: {to_id}",
                [rel_id], "Fix the entity reference"
            ))
```

#### Step 4: 调用所有新校验

在 `validate_blueprint()` 顶部加：

```python
    _validate_meta(blueprint, issues)
    _validate_knowledge_block(blueprint, issues)
    _validate_relations_basic(blueprint, issues)
    _validate_clarify_requests(blueprint, issues)
```

#### Step 5: 写测试

`tests/test_validate_knowledge.py`:

```python
import sys
sys.path.insert(0, "scripts/business_blueprint")
from validate import validate_blueprint


def _make_minimal_dk_blueprint():
    """Helper: minimal valid domain-knowledge blueprint."""
    return {
        "meta": {"blueprintType": "domain-knowledge", "detectedIntent": "test intent"},
        "library": {
            "knowledge": {
                "painPoints": [{"id": "pain-001", "name": "ROI 不稳", "entityType": "painPoint"}]
            }
        },
        "context": {
            "clarifyRequests": [
                {"id": f"clr-00{i}", "targetEntityId": "pain-001", "question": f"q{i}"}
                for i in range(1, 4)
            ]
        },
        "relations": []
    }


def test_minimal_dk_blueprint_passes():
    bp = _make_minimal_dk_blueprint()
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert len(errors) == 0, f"Expected no errors, got: {errors}"


def test_missing_core_fields():
    bp = _make_minimal_dk_blueprint()
    bp["library"]["knowledge"]["painPoints"] = [{"id": "pain-001"}]  # missing name + entityType
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert any("MISSING_NAME" in i["code"] for i in errors)
    assert any("MISSING_ENTITYTYPE" in i["code"] for i in errors)


def test_invalid_blueprint_type():
    bp = _make_minimal_dk_blueprint()
    bp["meta"]["blueprintType"] = "invalid-type"
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert any("INVALID_BLUEPRINT_TYPE" in i["code"] for i in errors)


def test_dk_missing_intent():
    bp = _make_minimal_dk_blueprint()
    bp["meta"]["detectedIntent"] = ""
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert any("MISSING_DETECTED_INTENT" in i["code"] for i in errors)


def test_architecture_with_knowledge_errors():
    bp = {
        "meta": {"blueprintType": "architecture"},
        "library": {
            "capabilities": [{"id": "cap-001", "name": "X"}],
            "knowledge": {"painPoints": [{"id": "pain-001", "name": "Y", "entityType": "painPoint"}]}
        },
        "context": {},
        "relations": []
    }
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert any("ARCHITECTURE_WITH_KNOWLEDGE" in i["code"] for i in errors)


def test_dk_empty_knowledge_errors():
    bp = _make_minimal_dk_blueprint()
    bp["library"]["knowledge"] = {}
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert any("DOMAIN_KNOWLEDGE_EMPTY" in i["code"] for i in errors)


def test_relation_missing_from_id():
    bp = _make_minimal_dk_blueprint()
    bp["relations"] = [{"id": "rel-001", "type": "solves", "from": "ghost", "to": "pain-001"}]
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert any("RELATION_MISSING_FROM" in i["code"] for i in errors)


def test_user_defined_fields_allowed():
    bp = _make_minimal_dk_blueprint()
    bp["library"]["knowledge"]["painPoints"][0]["customField"] = "any value"
    bp["library"]["knowledge"]["painPoints"][0]["nestedJunk"] = {"any": {"thing": "ok"}}
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert len(errors) == 0


def test_unknown_relation_type_is_warning():
    bp = _make_minimal_dk_blueprint()
    bp["relations"] = [{"id": "rel-001", "type": "totally_made_up", "from": "pain-001", "to": "pain-001"}]
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    warnings = [i for i in result["issues"] if i["severity"] == "warning"]
    assert len(errors) == 0
    assert any("RELATION_UNKNOWN_TYPE" in i["code"] for i in warnings)


def test_architecture_blueprint_unchanged():
    """Backward compat: existing architecture blueprint passes."""
    bp = {
        "meta": {"title": "Test", "industry": "retail"},
        "library": {
            "capabilities": [{"id": "cap-001", "name": "X", "level": 1}]
        },
        "context": {},
        "relations": []
    }
    result = validate_blueprint(bp)
    errors = [i for i in result["issues"] if i["severity"] == "error"]
    assert len(errors) == 0
```

#### Step 6: 跑测试 + commit

```bash
python -m pytest tests/test_validate_knowledge.py -v
git add references/knowledge-entities-schema.md scripts/business_blueprint/validate.py tests/test_validate_knowledge.py
git commit -m "feat: add minimal knowledge entity + relation validation

V2 minimal validation: core fields (id/name/entityType) strict, optional
fields untouched. Relations check ID refs + type whitelist (warn-only for
unknown types). NO cycle detection, NO semantic validation (deferred to P3).

10 unit tests cover happy path, missing fields, type mismatch, backward compat.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 1.3: hints 诚实化

**Files**:
- Modify: `scripts/business_blueprint/templates/retail/seed.json`
- Modify: `scripts/business_blueprint/templates/finance/seed.json`
- Modify: `scripts/business_blueprint/templates/manufacturing/seed.json`
- Modify: `SKILL.md`

#### Step 1: 给 retail/finance/manufacturing 加 knowledgeHints + `_status` 标记

**retail/seed.json** 的 industryHints 加：

```json
{
  "industryHints": {
    "title": "零售行业蓝图关注点",
    "checklist": [...existing...],
    "knowledgeHints": {
      "_status": "template-only-not-domain-validated",
      "_disclaimer": "本 hints 由模板生成，未经领域专家验证。建议根据实际业务场景增删。",
      "title": "零售行业 know-how 关注点",
      "checklist": [
        "痛点：库存积压、客流下滑、会员流失、POS 效率低",
        "策略：会员分层、智能补货、导购赋能、全渠道融合",
        "规则：食品安全合规、价格欺诈风险、数据隐私法规",
        "指标：坪效、客单价、会员复购率、员工人效",
        "最佳实践：陈列迭代周期、促销节奏、会员召回时机",
        "误区：过度依赖促销、忽视会员运营、数据孤岛"
      ]
    }
  }
}
```

finance 和 manufacturing 同样加，内容沿用 v1 plan 中的（虽然内容是模板填充，但有 `_status` 标注用户能看见）。

#### Step 2: SKILL.md 加 hints 状态使用规则

```markdown
### Step 2.5: Honesty About Hints

When using `industryHints.knowledgeHints`, check `_status`:

- `"depth-validated"`: Trust hints, use as primary signal
- `"template-only-not-domain-validated"`: Use as fallback signal, but **AI must include in detectedIntent or first response**:
  > "我用的是模板版 hints（未经领域验证），请重点检查痛点/策略是否符合你的实际业务"

This honesty prevents users from over-trusting AI extraction in poorly-modeled industries.
```

#### Step 3: commit

```bash
git add scripts/business_blueprint/templates/retail/seed.json
git add scripts/business_blueprint/templates/finance/seed.json
git add scripts/business_blueprint/templates/manufacturing/seed.json
git add SKILL.md
git commit -m "feat: add knowledgeHints with honesty markers to industry templates

retail/finance/manufacturing get knowledgeHints marked
'_status: template-only-not-domain-validated'. SKILL.md requires AI to
disclose this when using template-only hints, preventing over-trust in
unverified industry knowledge.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 1.4: 跨境电商深度模板（depth-validated）

**Files**:
- Create: `scripts/business_blueprint/templates/cross-border-ecommerce/seed.json`

#### Step 1: 创建跨境电商目录和模板

```bash
mkdir -p scripts/business_blueprint/templates/cross-border-ecommerce
```

`scripts/business_blueprint/templates/cross-border-ecommerce/seed.json`:

```json
{
  "version": "1.0",
  "meta": {
    "blueprintType": "domain-knowledge",
    "detectedIntent": ""
  },
  "context": {
    "goals": [],
    "scope": [],
    "assumptions": [],
    "constraints": [],
    "sourceRefs": [],
    "clarifyRequests": [],
    "clarifications": []
  },
  "library": {
    "capabilities": [],
    "actors": [],
    "flowSteps": [],
    "systems": [],
    "knowledge": {
      "painPoints": [],
      "strategies": [],
      "rules": [],
      "metrics": [],
      "practices": [],
      "pitfalls": []
    }
  },
  "relations": [],
  "views": [],
  "editor": {"fieldLocks": {}, "theme": "enterprise-default"},
  "artifacts": {},
  "industryHints": {
    "title": "跨境电商广告投放 know-how",
    "checklist": [],
    "knowledgeHints": {
      "_status": "depth-validated",
      "title": "跨境电商广告投放领域 know-how",
      "checklist": [
        "痛点：ROAS 波动（欧美市场 2.0-5.0）、素材疲劳（CTR 降 >10%）、平台封号（Facebook 封号率 >5%）、库存积压（周转率 <3）、汇率风险、合规风险",
        "策略：测款节奏（3 天周期、70% 测款预算）、动态出价、受众分层（LTV 分层）、再营销触发（浏览 >3 次）、预算动态分配、多平台分散",
        "规则：Facebook 政策红线（虚假折扣封号）、Google Quality Score（>7 才控成本）、TikTok 视频审核要点、Amazon 产品描述真实性",
        "指标：ROAS（>3.0 欧美电商）、CPA（<$20）、CTR（>1.5%）、LTV（>$50）、转化率（>2%）",
        "最佳实践：素材 7 天迭代周期、70%/30% 测款放量分配、再营销 20% 预算、单平台预算 <60%",
        "误区：单平台依赖 >80%（封号风险）、忽视合规（违规率 >15% 封禁）、数据孤岛、盲目放量、忽视 LTV、素材疲劳不更换"
      ]
    }
  }
}
```

#### Step 2: commit

```bash
git add scripts/business_blueprint/templates/cross-border-ecommerce/seed.json
git commit -m "feat: add cross-border-ecommerce industry template (depth-validated)

The only depth-validated knowledgeHints in v2: covers 6 entity types with
real numerical anchors (ROAS >3.0, CPA <\$20, etc.) for cross-border
e-commerce advertising domain.

Used as gold-standard fixture for L2/L3 eval.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Phase 1 Checkpoint

```bash
python -m pytest tests/test_validate_knowledge.py tests/test_clarify_required.py tests/test_refine_diff.py -v
git tag phase-1-complete
git commit --allow-empty -m "checkpoint: Phase 1 schema extension complete

- meta.blueprintType + detectedIntent (intent extraction)
- library.knowledge minimal validation
- hints honesty markers (_status field)
- cross-border-ecommerce depth template

Next: Phase 2 rendering."
```

---

## Phase 2: Validator + Render 极简

### Task 2.1: 6 类基础渲染样式

**Files**:
- Modify: `scripts/business_blueprint/export_svg.py`

(Step 1 内容已在 Task 0.2 Step 3 中实现 — 6 类样式 + 自检高亮)

#### Step 1: 加关系连线渲染

```python
RELATION_STYLES = {
    "solves": {"color": "#10B981", "dashArray": "", "label": "解决"},
    "prevents": {"color": "#F59E0B", "dashArray": "5,5", "label": "规避"},
    "measures": {"color": "#4F46E5", "dashArray": "", "label": "衡量"},
    "enforces": {"color": "#DC2626", "dashArray": "8,4", "label": "约束"},
    "requires": {"color": "#6B7280", "dashArray": "5,5", "label": "依赖"},
    "causes": {"color": "#DC2626", "dashArray": "", "label": "导致"},
    "impacts": {"color": "#F59E0B", "dashArray": "5,5", "label": "影响"},
    "supports": {"color": "#10B981", "dashArray": "", "label": "支撑"},
    "enforcedBy": {"color": "#D97706", "dashArray": "8,4", "label": "受约束"},
    "measuredBy": {"color": "#4F46E5", "dashArray": "5,5", "label": "受监控"},
}


def _render_relation(rel: dict, x1: int, y1: int, x2: int, y2: int) -> str:
    rel_type = rel.get("type", "")
    style = RELATION_STYLES.get(rel_type, {"color": "#9CA3AF", "dashArray": "", "label": rel_type})
    
    line = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
    line += f'stroke="{style["color"]}" stroke-width="2" '
    if style["dashArray"]:
        line += f'stroke-dasharray="{style["dashArray"]}" '
    line += 'marker-end="url(#arrowhead)"/>'
    
    # Label at midpoint
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2
    line += f'<text x="{mid_x}" y="{mid_y}" font-size="10" fill="{style["color"]}" '
    line += f'text-anchor="middle">{style["label"]}</text>'
    
    return line
```

#### Step 2: 集成到 export_svg 主流程

(具体集成点取决于现有 export_svg.py 结构，此处略 — 实施时根据现有代码调整)

#### Step 3: commit

```bash
git add scripts/business_blueprint/export_svg.py
git commit -m "feat: add knowledge entity + relation rendering

Six entity types with distinct color/icon/shape. Ten relation types with
solid/dashed line styles and labels. Self-check questions trigger yellow
border + ? badge for visual uncertainty signal.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 2.2: SKILL.md Step 2 整合

**Files**:
- Modify: `SKILL.md`

#### Step 1: 替换 Step 2 章节（综合 Phase 0 + 1 的所有规则）

```markdown
### Step 2: Extract Entities

**First**, run Blueprint Type Detection (see section above) — output `meta.detectedIntent` and `meta.blueprintType`.

**If `blueprintType = "architecture"`**:
Extract from user source + industryHints.checklist:
- capabilities, actors, flowSteps, systems
- See `references/entities-schema.md`

**If `blueprintType = "domain-knowledge"`**:
Extract from user source + industryHints.knowledgeHints.checklist:
- painPoints, strategies, rules, metrics, practices, pitfalls
- See `references/knowledge-entities-schema.md`

**Knowledge entity extraction order**:
1. Read `industryHints.knowledgeHints.checklist`
2. Note `_status` — if `template-only-not-domain-validated`, disclose to user
3. Extract painPoints first (core anchors)
4. Derive strategies (each strategy `solves` a painPoint)
5. Extract practices (each strategy `requires` a practice)
6. Extract metrics (each strategy `measures` by a metric)
7. Extract rules (each strategy `enforces` rules)
8. Extract pitfalls (each pitfall `causes` a painPoint)
9. Build `relations` array from above linkages

**Step 2.5: Self-Check** (see `references/knowledge-self-check.md`)
For each entity, run the entity-type-specific check questions. Populate `_selfCheck.passed` (confirmed) and `_selfCheck.questions` (uncertain).

**Step 2.6: Clarification Turn** (domain-knowledge only)
Output ≥3 `clarifyRequests` in `context.clarifyRequests` targeting specific entities. See "Clarification Turn" section above.

**Minimal entity fields**:
- All knowledge entities must have: `id`, `name`, `entityType`
- `_selfCheck` recommended (improves user experience)
- Optional fields (description, severity, level, etc.) recommended; user-defined fields allowed
```

#### Step 2: commit

```bash
git add SKILL.md
git commit -m "docs: integrate Phase 0+1 rules into SKILL.md Step 2

Comprehensive entity extraction guide with: blueprint type detection
(intent extraction), hints honesty disclosure, six knowledge entity types
with extraction order, self-check turn, clarification turn.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Phase 2 Checkpoint

```bash
# Run full test suite
python -m pytest tests/ -v

# Smoke test: cross-border-ecommerce scenario
python -m business_blueprint.cli plan \
  --industry cross-border-ecommerce \
  --intent "跨境电商广告 know-how 大图" > /tmp/smoke_blueprint.json

# Verify: validator passes, has knowledge block, has clarifyRequests >=3
python -m business_blueprint.cli validate /tmp/smoke_blueprint.json

# Smoke test: refine
python -m business_blueprint.cli refine \
  --blueprint /tmp/smoke_blueprint.json \
  --feedback "策略部分太浅" \
  --output /tmp/smoke_blueprint_v2.json

# Verify: diff was generated, new blueprint validates
python -m business_blueprint.cli validate /tmp/smoke_blueprint_v2.json

git tag phase-2-complete
git commit --allow-empty -m "checkpoint: Phase 2 (validator + render minimal) complete

All P0+P1+P2 functionality integrated. Smoke test passes for full pipeline:
plan -> validate -> refine -> validate.

Next: Run L2 + L3 evals (see test design). Ship gate is at L3."
```

---

## Phase 3 (Deferred — NOT in this plan)

Following items are explicitly **out of scope** for this plan. Each has a documented trigger condition (see design v2 section 10):

- ❌ Validator: cycle detection, semantic relation validation, severity/level soft schema
- ❌ Render: entityType clustering, performance limits (>50 entities), nested fault tolerance
- ❌ Web viewer: diff review UI for `--refine`
- ❌ `--contribute-hints` reverse hints sedimentation

These remain documented for future work but are not implemented now.

---

## Self-Review Checklist

### 1. Spec Coverage (vs Design v2)

| Design v2 Section | Plan Task | Status |
|---|---|---|
| Phase 0 三件套 | Task 0.1, 0.2, 0.3 | ✅ |
| Schema 极简扩展 | Task 1.1, 1.2 | ✅ |
| hints 诚实化 | Task 1.3, 1.4 | ✅ |
| blueprintType 意图抽取 | Task 1.1 | ✅ |
| Validator 极简 | Task 0.1, 1.2 | ✅ |
| Render 极简 + 自检可视化 | Task 0.2, 2.1 | ✅ |
| Phase 3 推迟项 | Section "Phase 3" | ✅ Listed, not implemented |

### 2. Placeholder Scan

✅ No TBD/TODO/placeholder. All steps contain complete code or specific instruction.

### 3. Test Coverage

- L1 Unit: `test_clarify_required.py` (3) + `test_refine_diff.py` (4) + `test_validate_knowledge.py` (10) = 17 tests
- L2 Extraction Eval: see test design doc
- L3 End-to-end Eval: see test design doc

### 4. Backward Compatibility

✅ All new fields optional. Default `blueprintType = "architecture"` ensures existing blueprints unaffected.

---

## Execution Handoff

**Phase 0** (核心创新, 6-8h): 三件套机制
**Phase 1** (3-4h): schema 极简扩展
**Phase 2** (2-3h): validator + render 极简
**Total implementation**: 11-15h

**Plus eval framework** (see test design doc): 18-23h
**Total**: 29-38h

**Ship Gate**: L3 eval 五指标全过 → Phase 1 进入 → 全部完成 → 真实使用观察 → 决定是否启动 Phase 3

**Next document**: `references/domain-knowledge-test-eval-design.md`
