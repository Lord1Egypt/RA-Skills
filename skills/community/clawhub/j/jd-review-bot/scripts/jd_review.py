"""
京东批量评价脚本 - 通过 browser-use CLI 自动评价所有待评价商品。

用法:
    python3 jd_review.py

依赖:
    - browser-use CLI
    - Chrome 浏览器已登录京东账号
"""

import subprocess
import json
import time
import random
import re
import sys
import shutil


def ensure_browser_use():
    """检查并安装 browser-use CLI"""
    if shutil.which("browser-use"):
        return True

    print("未检测到 browser-use，正在自动安装...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "browser-use"],
            check=True, capture_output=True, text=True
        )
        subprocess.run(
            ["browser-use", "install"],
            check=True, capture_output=True, text=True, timeout=120
        )
        print("browser-use 安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装 browser-use 失败: {e.stderr}")
        print("请手动安装: pip install browser-use && browser-use install")
        return False

# === 好评文字模板 (15-26字) ===
REVIEW_TEXTS = [
    "宝贝收到了质量很好做工精细非常满意的一次购物体验好评",
    "商品不错包装很严实物流也很快好评推荐购买",
    "质量很好价格实惠值得购买五星好评满意",
    "收到货了跟描述一样很满意以后还会再来好评",
    "东西挺好的用着很顺手推荐购买好评",
    "快递很快包装完好产品质量也不错好评推荐",
    "物美价廉性价比很高满意的一次购物体验",
    "用了一段时间了质量没问题好评推荐购买",
    "外观好看做工精致非常满意好评推荐",
    "第二次购买了质量稳定值得信赖好评",
    "物流超快东西也很好用点赞推荐购买",
    "性价比很高质量超出预期推荐好评",
    "服务态度很好物流速度很快整体体验非常满意",
    "安装师傅很专业态度很好非常满意的一次购物",
    "配送速度快包装完好安装服务也很到位好评",
]


def run(cmd_args, timeout=20):
    """执行 browser-use CLI 命令"""
    args = ["browser-use", "--browser", "real", "--headed", "--session", "jdreview"] + cmd_args
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()


def bu_open(url):
    """打开 URL"""
    run(["open", url])


def bu_type(text):
    """模拟键盘输入文字"""
    run(["type", text])


def bu_eval(js):
    """执行 JavaScript 并返回解析后的结果"""
    r = run(["--json", "eval", js])
    try:
        return json.loads(r).get("data", {}).get("result")
    except Exception:
        return r


def collect_all_ruleids():
    """遍历5页收集所有待评价订单 ruleid"""
    print("=== 收集待评价订单 ===")
    all_rids = []
    for page in range(1, 6):
        url = f"https://club.jd.com/myJdcomments/myJdcomment.action?sort=0&page={page}"
        bu_open(url)
        time.sleep(1.5)
        r = bu_eval("""
            Array.from(document.querySelectorAll('a'))
                .filter(a => a.textContent.trim() === '评价' && a.href.includes('orderVoucher'))
                .map(a => a.href.match(/ruleid=(\\d+)/)[1])
                .filter((v, i, a) => a.indexOf(v) === i)
        """)
        if r:
            all_rids.extend(r)
            print(f"  第 {page} 页: {len(r)} 条")

    all_rids = list(dict.fromkeys(all_rids))  # 去重保序
    print(f"共 {len(all_rids)} 件待评价\n")
    return all_rids


def rate_all_stars():
    """对所有 .commstar 评分组件执行五星好评"""
    return bu_eval("""
        (() => {
            let n = 0;
            document.querySelectorAll('.commstar').forEach(group => {
                for (let i = 1; i <= 5; i++) {
                    const star = group.querySelector('.star.star' + i);
                    if (star) {
                        star.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
                        star.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                    }
                }
                const s5 = group.querySelector('.star.star5');
                if (s5) { s5.dispatchEvent(new MouseEvent('click', { bubbles: true })); n++; }
            });
            return n;
        })()
    """)


def fill_all_textareas():
    """对每个可见 textarea 逐一聚焦并用 browser-use type 输入文字"""
    ta_count_str = bu_eval("""
        (() => {
            const allTA = Array.from(document.querySelectorAll('textarea'))
                .filter(t => window.getComputedStyle(t).display !== 'none');
            return allTA.length;
        })()
    """)
    try:
        ta_count = int(ta_count_str)
    except (ValueError, TypeError):
        ta_count = 0

    filled = []
    for idx in range(ta_count):
        text = random.choice(REVIEW_TEXTS)
        bu_eval(f"""
            (() => {{
                const allTA = Array.from(document.querySelectorAll('textarea'))
                    .filter(t => window.getComputedStyle(t).display !== 'none');
                const ta = allTA[{idx}];
                if (ta) {{ ta.focus(); ta.click(); ta.value = ''; return 'ok'; }}
                return 'miss';
            }})()
        """)
        time.sleep(0.2)
        bu_type(text)
        time.sleep(0.3)
        filled.append(str(len(text)))
    return filled


def handle_service_impressions():
    """如果有服务印象标签，选中 2-3 个正面标签"""
    return bu_eval("""
        (() => {
            const section = document.querySelector('.fop-reasons');
            if (!section) return 'no_reasons';
            const labels = section.querySelectorAll('label, span');
            const positive = Array.from(labels).filter(l => {
                const t = l.textContent.trim();
                return t.includes('态度好') || t.includes('速度快') || t.includes('专业')
                    || t.includes('满意') || t.includes('耐心') || t.includes('及时')
                    || t.includes('热情') || t.includes('细心') || t.includes('准时');
            });
            positive.slice(0, 3).forEach(l => l.click());
            return 'clicked_' + Math.min(3, positive.length);
        })()
    """)


def sync_counters():
    """将 textarea 的实际文字长度同步到京东的字符计数器"""
    bu_eval("""
        (() => {
            document.querySelectorAll('textarea').forEach(ta => {
                const container = ta.closest('.fop-item');
                const counterB = container?.querySelector('.textarea-num b');
                if (counterB && ta.value.length > 0) {
                    counterB.textContent = ta.value.length;
                }
            });
        })()
    """)


def click_submit():
    """点击发表按钮"""
    return bu_eval("""
        (() => {
            const btn = Array.from(document.querySelectorAll('a'))
                .find(el => el.textContent.trim() === '发表');
            if (btn) { btn.click(); return 'submit_ok'; }
            return 'no_btn';
        })()
    """)


def verify_submission():
    """检查评价是否成功（页面是否跳转离开评价页）"""
    result = bu_eval("""
        (() => {
            const body = document.body.innerText;
            if (!body.includes('评价订单')) return 'SUCCESS';
            if (body.includes('请填写完整的评价内容')) return 'ERROR_fill';
            if (body.includes('请至少填写')) return 'ERROR_star';
            return 'UNKNOWN';
        })()
    """)
    return str(result) if result else "?"


def review_one(ruleid, index, total):
    """评价单个商品"""
    review_url = f"https://club.jd.com/myJdcomments/orderVoucher.action?ruleid={ruleid}"
    print(f"[{index}/{total}] {ruleid}", end=" ", flush=True)

    bu_open(review_url)
    time.sleep(2.5)

    # Step 1: 先填文字（关键顺序！）
    filled = fill_all_textareas()
    print(f"t={','.join(filled)}", end=" ", flush=True)

    # Step 2: 同步计数器
    sync_counters()
    time.sleep(0.3)

    # Step 3: 评分
    stars = rate_all_stars()
    print(f"s={stars}", end=" ", flush=True)
    time.sleep(0.5)

    # Step 4: 服务印象
    reasons = handle_service_impressions()
    time.sleep(0.3)

    # Step 5: 再次同步计数器（评分可能清空 textarea）
    sync_counters()

    # Step 6: 提交
    submit = click_submit()
    print(f"sub={submit}", end=" ", flush=True)
    time.sleep(2.5)

    # Step 7: 验证
    result = verify_submission()
    print(f"=> {result}")

    return "SUCCESS" in result


def main():
    print("=" * 50)
    print("京东批量评价脚本")
    print("=" * 50)

    # 环境检查
    if not ensure_browser_use():
        sys.exit(1)

    # 阶段 1: 收集
    ruleids = collect_all_ruleids()
    if not ruleids:
        print("没有待评价订单！")
        return

    # 阶段 2: 批量评价
    print(f"=== 开始批量评价 ({len(ruleids)} 件) ===\n")
    done = 0
    fail = 0

    for i, rid in enumerate(ruleids, 1):
        try:
            if review_one(rid, i, len(ruleids)):
                done += 1
            else:
                fail += 1
        except Exception as e:
            print(f"  EXCEPTION: {e}")
            fail += 1

        # 随机延迟避免被限流
        time.sleep(random.uniform(1.5, 3))

    # 阶段 3: 结果
    print(f"\n{'=' * 50}")
    print(f"评价完成! 成功: {done}  失败: {fail}")
    print(f"{'=' * 50}")

    # 验证
    print("\n=== 验证最终结果 ===")
    bu_open("https://club.jd.com/myJdcomments/myJdcomment.action")
    time.sleep(2)
    remaining = bu_eval("""
        Array.from(document.querySelectorAll('a'))
            .filter(a => a.textContent.trim() === '评价' && a.href.includes('orderVoucher'))
            .length
    """)
    print(f"第 1 页剩余待评价: {remaining}")
    if remaining and int(remaining) == 0:
        print("全部评价完成！")


if __name__ == "__main__":
    main()
