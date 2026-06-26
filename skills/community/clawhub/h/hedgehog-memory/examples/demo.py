"""
radial_memory/demo.py
─────────────────────────────────────────────────────────
完整演示：单条线 + 多条线的全流程

运行方式:
    python -m radial_memory.demo
    或
    cd radial_memory && python demo.py
"""

from __future__ import annotations

import shutil
import textwrap
from pathlib import Path

from .memory import RadialMemory
from .context_manager import ContextWindowManager


DEMO_DIR = "./demo_memory_store"
SEP = "─" * 64


def banner(title: str) -> None:
    print(f"\n{'═' * 64}")
    print(f"  {title}")
    print(f"{'═' * 64}")


def section(title: str) -> None:
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)


# ─────────────────────────────────────────────
# 演示 1：单条线完整流程
# ─────────────────────────────────────────────

def demo_single_line():
    banner("演示 1：单条线完整流程（auth 认证模块）")

    mem = RadialMemory(DEMO_DIR, project_name="电商推荐系统")

    # 创建任务线
    mem.create_line("auth", "认证模块", "用户登录/注册、JWT、权限验证")

    section("① 初始原点上下文（空线）")
    print(mem.get_origin_context())

    # ── 任务 1：agent 完成 JWT 登录接口 ──────────────────────────
    section("② 任务 1 完成：实现 JWT 登录接口")

    mem.complete_task(
        line_id="auth",
        task_label="实现 JWT 登录接口",
        full_context=textwrap.dedent("""\
            项目: 电商推荐系统  模块: auth
            ===== 完整工作上下文 =====
            已实现 POST /api/auth/login 接口。
            接受 {username, password}，验证后返回 {access_token, refresh_token}。
            access_token 有效期 15 分钟，refresh_token 7 天。
            使用 PyJWT 库，SECRET_KEY 存于 .env。
            auth/views.py > login() 函数已通过 Postman 手动测试。
            待补充：单元测试、限流中间件。
        """),
        conversation_summary=(
            "讨论了 JWT vs Session 的取舍，最终选 JWT 无状态方案。"
            "实现了 /login 接口，access_token=15min refresh_token=7d。"
            "使用 PyJWT，密钥存 .env。Postman 测试通过。"
        ),
        modified_files=[
            {"path": "auth/views.py",    "change_type": "modified", "diff_summary": "新增 login() 视图函数"},
            {"path": "auth/serializers.py", "change_type": "modified", "diff_summary": "新增 LoginSerializer"},
            {"path": "config/settings.py",  "change_type": "modified", "diff_summary": "添加 JWT_SECRET_KEY 配置"},
            {"path": ".env.example",     "change_type": "created",  "diff_summary": "添加 JWT_SECRET_KEY 示例"},
        ],
        env_info={"python": "3.11", "PyJWT": "2.8.0", "django": "4.2"},
        todos=["补充 login 单元测试", "添加登录限流（5次/分钟）", "实现 /refresh_token 接口"],
    )

    section("② 完成后的原点上下文")
    print(mem.get_origin_context())

    # ── 任务 2：agent 完成 refresh_token 接口 ────────────────────
    section("③ 任务 2 完成：实现 refresh_token 接口")

    mem.complete_task(
        line_id="auth",
        task_label="实现 refresh_token 刷新接口",
        full_context=textwrap.dedent("""\
            项目: 电商推荐系统  模块: auth
            ===== 完整工作上下文 =====
            新增 POST /api/auth/refresh 接口。
            接受 {refresh_token}，校验签名和过期，返回新 {access_token}。
            refresh_token 本身不轮换（若需安全加固可改为轮换模式）。
            auth/views.py > refresh_token() 已实现并通过单元测试。
            同时补充了 login 的 3 个单元测试（正常登录、密码错误、用户不存在）。
        """),
        conversation_summary=(
            "实现了 /refresh 接口，校验 refresh_token 签名后返回新 access_token。"
            "顺带补全了 login 的单元测试（3 个用例全过）。"
            "限流中间件留到下次完成。"
        ),
        modified_files=[
            {"path": "auth/views.py",    "change_type": "modified", "diff_summary": "新增 refresh_token() 视图"},
            {"path": "auth/urls.py",     "change_type": "modified", "diff_summary": "注册 /refresh 路由"},
            {"path": "auth/tests.py",    "change_type": "created",  "diff_summary": "新增 login 和 refresh 单元测试"},
        ],
        env_info={"python": "3.11", "PyJWT": "2.8.0", "django": "4.2"},
        todos=["添加登录限流（5次/分钟）", "考虑 refresh_token 轮换策略"],
    )

    section("③ 完成两个任务后的原点上下文")
    print(mem.get_origin_context())

    # ── 任务 3：添加限流 ──────────────────────────────────────────
    section("④ 任务 3 完成：添加登录限流中间件")

    mem.complete_task(
        line_id="auth",
        task_label="添加登录限流中间件",
        full_context=textwrap.dedent("""\
            项目: 电商推荐系统  模块: auth
            ===== 完整工作上下文 =====
            使用 django-ratelimit 实现登录限流：5次/分钟/IP。
            超限返回 429 Too Many Requests。
            中间件挂在 /api/auth/login 路由上。
            已在 staging 环境验证通过。
        """),
        conversation_summary=(
            "引入 django-ratelimit 实现 /login 接口限流，5次/分钟/IP。"
            "超限返回 429。staging 验证通过。auth 模块主要功能完成。"
        ),
        modified_files=[
            {"path": "auth/views.py",      "change_type": "modified", "diff_summary": "添加 @ratelimit 装饰器"},
            {"path": "requirements.txt",   "change_type": "modified", "diff_summary": "添加 django-ratelimit==4.1.0"},
        ],
        env_info={"python": "3.11", "django": "4.2", "django-ratelimit": "4.1.0"},
        todos=["refresh_token 轮换策略（优先级低）"],
    )

    section("④ 完成三个任务后的原点上下文")
    print(mem.get_origin_context())

    # ── 演示线历史 ────────────────────────────────────────────────
    section("⑤ auth 线完整历史（从新到旧）")
    history = mem.get_line_history("auth")
    for entry in history:
        print(f"  pos={entry['position']}  [{entry['created_at']}]  {entry['task_label']}")
        print(f"    L0: {entry['l0_summary']}")
        print(f"    L1: {entry['l1_summary'][:100]}...")
        print()

    # ── 演示导航 ──────────────────────────────────────────────────
    section("⑥ 导航：查找「JWT 登录」相关任务")
    session = mem.navigate("JWT 登录接口", line_id="auth")
    if session:
        print(session.context)
        print(f"\n→ 是否有更多细节可钻取: {session.needs_more_detail}")
        if session.needs_more_detail:
            section("  钻取到 L2（summary 层级）")
            session2 = session.drill_deeper()
            print(session2.context)
    else:
        print("未找到匹配节点。")

    section("⑦ 直接载入最新节点 L3（detailed）完整上下文")
    print(mem.load_node_context("auth", position=1, level=3))


# ─────────────────────────────────────────────
# 演示 2：多条线 + 跨线感知
# ─────────────────────────────────────────────

def demo_multi_line():
    banner("演示 2：多条线（auth + rec + infra）")

    mem = RadialMemory(DEMO_DIR, project_name="电商推荐系统")

    # auth 线已存在，再创建两条
    mem.get_or_create_line("rec",   "推荐引擎", "协同过滤、向量召回、重排序")
    mem.get_or_create_line("infra", "基础设施", "Docker、CI/CD、监控告警")

    # ── 推荐引擎：任务 1 ──────────────────────────────────────────
    mem.complete_task(
        line_id="rec",
        task_label="实现用户协同过滤基线",
        full_context="rec 模块：基于用户行为矩阵的协同过滤，使用 surprise 库，RMSE=0.82",
        conversation_summary=(
            "实现了基于 user-item 矩阵的协同过滤，使用 surprise 库的 SVD 算法，"
            "RMSE 0.82，作为推荐基线。"
        ),
        modified_files=[
            {"path": "rec/cf_model.py", "change_type": "created",  "diff_summary": "协同过滤模型实现"},
            {"path": "rec/train.py",    "change_type": "created",  "diff_summary": "训练脚本"},
        ],
        todos=["接入实时用户行为流", "尝试 ALS 算法对比"],
    )

    # ── 基础设施：任务 1 ──────────────────────────────────────────
    mem.complete_task(
        line_id="infra",
        task_label="搭建 Docker 容器化部署",
        full_context="infra：Dockerfile + docker-compose，支持 web/celery/redis 三服务编排",
        conversation_summary=(
            "编写了 Dockerfile 和 docker-compose.yml，包含 web/celery/redis 三个服务。"
            "本地一键 docker-compose up 验证通过。"
        ),
        modified_files=[
            {"path": "Dockerfile",            "change_type": "created",  "diff_summary": "多阶段构建镜像"},
            {"path": "docker-compose.yml",    "change_type": "created",  "diff_summary": "三服务编排"},
        ],
        todos=["配置 GitHub Actions CI", "添加健康检查"],
    )

    section("多线原点概况（一次看清全局）")
    print(mem.get_origin_context())

    section("所有任务线列表")
    for line_info in mem.list_lines():
        print(
            f"  [{line_info['id']:6s}] {line_info['name']:8s} "
            f"nodes={line_info['node_count']}  "
            f"latest='{line_info['latest_task']}'"
        )

    section("跨线导航：搜索「部署相关任务」（搜索全部线）")
    session = mem.navigate("docker 部署容器")
    if session:
        print(session.context)
    else:
        print("未找到，尝试降低阈值...")
        session = mem.navigate("部署", confidence_threshold=0.1)
        if session:
            print(session.context)


# ─────────────────────────────────────────────
# 演示 3：步进导航（agent 手动控制）
# ─────────────────────────────────────────────

def demo_step_navigation():
    banner("演示 3：步进导航（模拟 agent 手动判断每个候选节点）")

    mem = RadialMemory(DEMO_DIR, project_name="电商推荐系统")

    nav = mem.navigate_step_by_step("登录限流")
    print(f"候选节点总数: {nav.remaining + 1}")

    step = 0
    while True:
        candidate = nav.next()
        if candidate is None:
            print("  → 已遍历所有候选，未找到匹配。")
            break
        step += 1
        print(f"\n--- 候选 {step} | 任务: {candidate.node.task_label} ---")
        # 模拟 agent 判断：task_label 含"限流"则认为匹配
        if "限流" in candidate.node.task_label:
            print("  [OK] Agent 判断匹配！继续钻取到 L2...")
            session = candidate.drill_deeper()
            print(session.context)
            break
        else:
            print(f"  [--] 不匹配，跳过。L1 摘要: {candidate.node.summaries.get(1,'')[:60]}...")


# ─────────────────────────────────────────────
# 演示 4：ContextWindowManager 完整循环
# ─────────────────────────────────────────────

def demo_context_manager():
    banner("演示 4：ContextWindowManager 完整循环（清空→原点→导航→100%还原）")

    mem = RadialMemory(DEMO_DIR, project_name="电商推荐系统")
    cw = ContextWindowManager(mem)

    # ── 步骤 1：清空上下文，仅注入原点 ──────────────────────────────
    section("步骤 1：reset() — 清空上下文窗口，仅保留原点结构")
    minimal_ctx = cw.reset()
    print(minimal_ctx)
    print(f"\n  → token 消耗约 {len(minimal_ctx)} 字符（相比完整状态大幅压缩）")

    # ── 步骤 2：agent 接收用户问题，导航寻找节点 ─────────────────────
    section("步骤 2：load() — 按用户问题导航，获取 L1 brief 供 agent 验证")
    result = cw.load("JWT 登录", line_id="auth")
    print(f"  status:     {result.status}")
    print(f"  匹配置信度: {result.match_confidence:.0%}")
    print(f"  当前层级:   L{result.current_level}")
    print(f"  可继续钻取: {result.can_drill_deeper}")
    print()
    print(result.context)

    # ── 步骤 3：agent 确认节点正确，继续钻取到 L2 ───────────────────
    section("步骤 3：drill_deeper() — agent 确认节点方向正确，钻取 L2")
    result_l2 = result.drill_deeper()
    print(f"  当前层级: L{result_l2.current_level}")
    print(result_l2.context)

    # ── 步骤 4：100% 还原完整工作状态（L4）─────────────────────────
    section("步骤 4：load_full_state() — 100% 还原完整工作状态")
    full = result_l2.load_full_state()
    print(f"  完整状态字符串长度: {len(full)} 字符")
    print("  +-- 内容预览 ----------------------------------------")
    for line in full.splitlines():
        print(f"  |  {line}")
    print("  +----------------------------------------------------")

    # ── 步骤 5：直接按 position 精确载入（已知节点时使用）──────────
    section("步骤 5：load_node() — 直接按 line+position 精确载入（无需导航）")
    result_direct = cw.load_node("auth", position=2, level=2)
    print(f"  载入节点: {result_direct.node.task_label if result_direct.node else 'N/A'}")
    print(result_direct.context)

    # ── 步骤 6：commit 新任务（写入新节点） ─────────────────────────
    section("步骤 6：commit() — agent 判断任务完成，写入新节点到永久文件")
    node = cw.commit(
        line_id="auth",
        task_label="添加邮件验证码登录",
        full_context=textwrap.dedent("""\
            项目: 电商推荐系统  模块: auth
            ===== 完整工作上下文 =====
            新增 POST /api/auth/login-with-code 接口。
            用户输入手机号后，后端发送 6 位验证码（TTL 5 分钟）。
            验证成功后同样返回 access_token + refresh_token。
            验证码存 Redis，键名 sms_code:{phone}，过期自动清除。
        """),
        conversation_summary="新增邮件/短信验证码登录接口，验证码存 Redis，TTL 5 分钟。",
        modified_files=[
            {"path": "auth/views.py",   "change_type": "modified", "diff_summary": "新增 login_with_code() 视图"},
            {"path": "auth/sms.py",     "change_type": "created",  "diff_summary": "短信/邮件验证码发送封装"},
            {"path": "auth/urls.py",    "change_type": "modified", "diff_summary": "注册 /login-with-code 路由"},
        ],
        todos=["接入真实短信服务商 API", "添加验证码发送频率限制"],
    )
    print(f"  [OK] 新节点已写入永久文件")
    print(f"    节点 ID:    {node.id}")
    print(f"    position:   {node.position}  （最靠近原点，最新最清晰）")
    print(f"    task_label: {node.task_label}")

    # ── 步骤 7：commit 后的原点（自动更新）─────────────────────────
    section("步骤 7：commit 后 reset() 验证 — 原点已自动更新")
    print(cw.reset())
    print(f"\n  状态报告:\n{cw.status_report()}")

    section("auth 线现在共有的节点（从新到旧）")
    for entry in mem.get_line_history("auth"):
        print(f"  pos={entry['position']}  {entry['task_label']:30s}  [{entry['created_at']}]")


# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────

def main():
    # 清除旧演示数据
    demo_path = Path(DEMO_DIR)
    if demo_path.exists():
        shutil.rmtree(demo_path)

    demo_single_line()
    demo_multi_line()
    demo_step_navigation()
    demo_context_manager()

    banner("演示完成！持久化文件位于: " + DEMO_DIR)
    print("  origin.json  （完整记忆体，可查看所有节点的多级摘要和状态快照）\n")


if __name__ == "__main__":
    main()
