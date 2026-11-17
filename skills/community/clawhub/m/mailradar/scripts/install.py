# -*- coding: utf-8 -*-
"""飞书邮件看板 一键安装 + 建每日自动化。

一键完成：
  1) 检查前置（Python / lark-cli / 飞书连接）
  2) 交互式生成 scripts/config.json（或复用已有）
  3) 幂等注册「每日邮件看板」自动化到 ~/.workbuddy/workbuddy.db
     （默认每天 08:00，FREQ=DAILY;BYHOUR=8;BYMINUTE=0，可用 --hour 改）

用法：
  python install.py                     # 交互式
  python install.py --no-automation     # 只建 config，不注册自动化
  python install.py --hour 9            # 每天 09:00
  python install.py --name 张三 --mailbox a@b.com --open-id ou_xxx
                                        # 非交互，直接写 config
"""
import json, os, sys, time, sqlite3, datetime

WS = os.path.dirname(os.path.abspath(__file__))
DB = os.path.expanduser('~/.workbuddy/workbuddy.db')
AUTO_NAME = '每日邮件看板推送'


def ask(prompt, default=''):
    sys.stdout.write(prompt + ((' [' + default + ']') if default else '') + ': ')
    sys.stdout.flush()
    v = sys.stdin.readline().strip()
    return v or default


def ensure_config(name=None, mailbox=None, open_id=None, push=True):
    """生成/复用 config.json，返回 dict。"""
    cfg_path = os.path.join(WS, 'config.json')
    cfg = {}
    if os.path.exists(cfg_path):
        try:
            cfg = json.load(open(cfg_path, encoding='utf-8')) or {}
        except Exception:
            cfg = {}
    changed = False
    if not name:
        name = ask('你的飞书昵称（用于 @提醒）', cfg.get('feishu_name', ''))
    if not mailbox:
        mailbox = ask('你的飞书邮箱地址', cfg.get('mailbox', ''))
    if not open_id:
        open_id = ask('接收推送的飞书 open_id（留空=只本地生成不推送）', cfg.get('feishu_open_id', ''))
    cfg['feishu_name'] = name or cfg.get('feishu_name', '同事')
    cfg['mailbox'] = mailbox or cfg.get('mailbox', 'your-name@company.com')
    cfg['feishu_open_id'] = open_id if open_id else cfg.get('feishu_open_id', '')
    cfg['push_enabled'] = True
    json.dump(cfg, open(cfg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('✔ config.json 已写入：%s' % cfg_path)
    return cfg


def check_prereqs():
    """返回 (ok, msgs)。"""
    msgs = []
    # Python 版本
    msgs.append('Python %s' % sys.version.split()[0])
    # lark-cli
    import shutil
    lark = shutil.which('lark-cli')
    if lark:
        msgs.append('lark-cli 可用：%s' % lark)
    else:
        msgs.append('⚠ lark-cli 未找到 —— 请先在工作台连接「飞书」连接器')
    return msgs


def _now_ms():
    return int(time.time() * 1000)


def _next_8am(hour=8):
    now = datetime.datetime.now()
    target = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if target <= now:
        target += datetime.timedelta(days=1)
    return int(target.timestamp() * 1000)


def find_owner(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT owner_user_id, COUNT(*) FROM automations "
                    "WHERE owner_user_id IS NOT NULL AND owner_user_id != '' "
                    "GROUP BY owner_user_id ORDER BY COUNT(*) DESC LIMIT 1")
        row = cur.fetchone()
        return row[0] if row else ''
    except Exception:
        return ''


def automation_exists(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT id FROM automations WHERE name=? AND (deleted_at IS NULL OR deleted_at=0)",
                    (AUTO_NAME,))
        return cur.fetchone() is not None
    except Exception:
        return False


def register_automation(hour=8, prompt=None):
    if not os.path.exists(DB):
        print('⚠ 未找到 workbuddy.db（%s），跳过自动化注册。' % DB)
        print('  请在 WorkBuddy 里手动建每日自动化，提示词见 deploy.md。')
        return False
    con = sqlite3.connect(DB, timeout=10)
    try:
        if automation_exists(con):
            print('✔ 已存在自动化「%s」，跳过重复注册。' % AUTO_NAME)
            return True
        owner = find_owner(con) or '1d6b34b8-cb1d-4b9a-a3a4-fcf423733ebc'
        now = _now_ms()
        nxt = _next_8am(hour)
        auto_id = 'automation-%d' % now
        if prompt is None:
            prompt = (
                '使用 feishu-mail-workboard 技能刷新并推送今日邮件看板（含中文摘要）。'
                '在技能 scripts 目录下依次执行：'
                '1) python daily_mail_board.py（拉取近7天飞书邮件→生成看板→推送飞书卡片+HTML附件）；'
                '2) python build_cn_inbox.py（生成待译清单 cn_inbox.json）；'
                '3) python cn_translate.py 导出待译邮件，按 references/cn-translate.md 规则译成中文，产出译文 JSON；'
                '4) python cn_translate.py --apply 译文.json 写回 workboard2_cn.json；'
                '5) PUSH_TAG=-cn python daily_mail_board.py --skip-pull（用新鲜译文重推含中文摘要的看板）。'
                '若当日无新邮件，仅执行 2-4 步补译、跳过重复推送。'
            )
        row = dict(
            id=auto_id, name=AUTO_NAME, prompt=prompt, status='ACTIVE',
            schedule_type='recurring', next_run_at=nxt, last_run_at=now,
            cwds=json.dumps([WS], ensure_ascii=False),
            rrule='FREQ=DAILY;BYHOUR=%d;BYMINUTE=0' % hour,
            scheduled_at=None, valid_from=None, valid_until=None,
            model_id='auto', model_is_thinking=1, push_to_wechat=0,
            created_at=now, updated_at=now,
            skills_json=json.dumps(['飞书邮件工作看板'], ensure_ascii=False),
            deleted_at=None, expert_id=None, expert_marketplace=None,
            connector_ids_json=json.dumps(['feishu'], ensure_ascii=False),
            permission_mode='fullAccess', owner_user_id=owner,
            owner_status='inferred', owner_source='history_unique',
            push_to_wecom_bot=0, wecom_bot_source=None,
        )
        cols = ', '.join(row.keys())
        ph = ', '.join('?' * len(row))
        con.execute('INSERT INTO automations (%s) VALUES (%s)' % (cols, ph), list(row.values()))
        con.commit()
        print('✔ 已注册每日自动化「%s」（每天 %02d:00，rrule=%s）' % (AUTO_NAME, hour, row['rrule']))
        print('  cwds = %s' % row['cwds'])
        return True
    except Exception as e:
        print('⚠ 自动化注册失败：%s' % e)
        print('  可手动在 WorkBuddy 建每日自动化，提示词见 deploy.md。')
        return False
    finally:
        con.close()


def main():
    args = sys.argv[1:]
    hour = 8
    if '--hour' in args:
        hour = int(args[args.index('--hour') + 1])
    no_auto = '--no-automation' in args
    # 非交互参数
    name = mailbox = open_id = None
    for flag in ('--name', '--mailbox', '--open-id'):
        if flag in args:
            v = args[args.index(flag) + 1]
            if flag == '--name':
                name = v
            elif flag == '--mailbox':
                mailbox = v
            else:
                open_id = v

    print('==============================================')
    print(' 飞书邮件工作看板 · 一键安装')
    print('==============================================')

    msgs = check_prereqs()
    for m in msgs:
        print('  · %s' % m)
    print('')

    cfg = ensure_config(name=name, mailbox=mailbox, open_id=open_id)

    print('')
    if not no_auto:
        register_automation(hour=hour)
    else:
        print('（--no-automation：跳过自动化注册）')

    print('')
    print('=============== 安装完成 ===============')
    print('下一步：')
    print('  1. 先本地预览：  python %s --no-push' % os.path.join(WS, 'daily_mail_board.py'))
    print('  2. 真推飞书：     python %s' % os.path.join(WS, 'daily_mail_board.py'))
    print('  3. 中文翻译：     python %s --full | 翻译后 python %s --apply 译文.json'
          % (os.path.join(WS, 'cn_translate.py'), os.path.join(WS, 'cn_translate.py')))
    if cfg.get('feishu_open_id'):
        print('  4. 每日自动化已就绪，每天 %02d:00 自动跑。' % hour)
    else:
        print('  4. 未填 open_id，只本地生成；填好后再跑一次本脚本注册推送。')


if __name__ == '__main__':
    main()
