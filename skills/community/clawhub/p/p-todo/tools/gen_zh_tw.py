# -*- coding: utf-8 -*-
"""生成 texts_zh_tw.properties：简体→繁体自动转换 + 人工修正"""
import io, sys
import zhconv

BASE = "src/main/resources/i18n"

# 需要人工修正的键（zhconv 转换不理想或需要繁体特定用词）
OVERRIDES = {
    # 名称/品牌保持不变
    "app.title": "P的事",
    "about.title": "關於 P的事",
    "about.subtitle": "P的事 — 團隊待辦管理",
    "about.creator.name": "Pondsi",
    "about.version": "v1.0.0-alpha",
    "about.build": "建置時間：2026-08-24",
    "about.creator.tech": "技術棧貢獻：MiMo（小米大模型）+ Qwen3.8-27B（通義千問）",
    "about.license.line10": "  • 如果是整體項目由此改造，請在關於頁面或文檔中註明「基於 P的事 改造」",
    # 用词差异（台湾繁体习惯）
    "detail.meta": "元資訊",
    "nav.workbench": "📊 工作台",
    "nav.myTasks": "📋 我的任務",
    "view.title.myTasks": "我的任務",
    "topbar.new": "+ 新增",
    "newTodo.create": "創 建",
    "newTodo.title": "新增待辦 - 團隊待辦",
    "shortcut.new": "新增待辦",
    "shortcut.newSection": "新增待辦",
    "mini.sortHint": "按緊急度排序：進行中 → 超時 → 延後 → 未開始 → 已完成",
    "settings.add": "新增",
    "settings.addLabel": "新增:",
    "settings.newMember": "新增成員",
    "settings.addHint": "輸入新成員名稱",
    "stats.format": "共 %d 項 | 完成 %d | 超時 %d",
    "about.usage.line1": "新增任務：點擊頂欄「+ 新增」或按 Ctrl+N",
    "calendar.monday": "週一",
    "calendar.tuesday": "週二",
    "calendar.wednesday": "週三",
    "calendar.thursday": "週四",
    "calendar.friday": "週五",
    "calendar.saturday": "週六",
    "calendar.sunday": "週日",
    "shortcut.example3": "例如: 項目 8月25日",
    "shortcut.example3desc": "截止日期=8月25日",
    "search.title": "全域搜尋 - 團隊待辦",
    "topbar.searchHint": "搜尋任務…",
    "search.hint": "🔍 輸入關鍵字，搜尋標題或描述…（Esc 關閉）",
    "common.unnamed": "（未命名）",
    "detail.noTitle": "（無標題）",
    "detail.noDesc": "（無描述）",
    "mini.noTodo": "（暫無待辦）",
    "kanban.empty": "（空）",
    "newTodo.assigneeHint": "（不指派）",
    "detail.selectFirst": "請先選擇一條任務",
    "settings.selectLanguage": "選擇語言",
    "dialog.inputName": "輸入你的名字",
    "claim.inputName": "輸入你的名字",
    "newTodo.desc": "描述",
    "detail.comments": "評論",
    "settings.notification": "通知音效",
    "settings.data": "資料",
    "settings.dataPath": "資料庫路徑: %s",
    "settings.exportJson": "匯出 JSON",
    "settings.exportCsv": "匯出 CSV",
    "settings.exportJsonTitle": "匯出 JSON",
    "settings.exportCsvTitle": "匯出 CSV",
    "settings.exported": "已匯出到: %s",
    "settings.exportFailed": "匯出失敗: %s",
    "about.section.agent": "🤖 智慧體（Agent）呼叫說明",
    "about.agent.line1": "本應用內建 REST API 服務，支援被外部 AI 智慧體或腳本呼叫。",
    "about.agent.line2": "API 服務位址：http://localhost:%d",
    "about.agent.line3": "可在「設定」頁面修改監聽連接埠，修改後需重啟應用。",
    "about.agent.line4": "介面列表：",
    "about.agent.line5": "  GET    /api/health           — 健康檢查",
    "about.agent.line6": "  GET    /api/todos            — 取得所有任務",
    "about.agent.line7": "  GET    /api/todos?status=IN_PROGRESS — 按狀態篩選",
    "about.agent.line8": "  POST   /api/todos            — 建立任務（JSON body）",
    "about.agent.line9": "  PUT    /api/todos/{id}       — 更新任務",
    "about.agent.line10": " DELETE /api/todos/{id}       — 刪除任務",
    "about.agent.line11": " PUT    /api/todos/{id}/toggle — 切換完成狀態",
    "about.agent.line12": " GET    /api/users            — 取得所有使用者",
    "about.agent.line13": " POST   /api/users            — 建立使用者",
    "about.agent.line14": " GET    /api/stats            — 取得統計資料",
    "about.agent.line15": "呼叫方式：curl、HTTP 客戶端、OpenClaw exec 等均可，無需認證。",
    "about.agent.line16": "範例：curl http://localhost:%d/api/todos",
    "about.perm.line1": "本應用完全本機執行，所有資料儲存在本機 SQLite 資料庫中。",
    "about.perm.line2": "不聯網、不上傳任何使用者資料到外部伺服器。",
    "about.perm.line3": "無需註冊帳號，安裝即用。",
    "about.perm.line4": "API 連接埠預設僅監聽 127.0.0.1（localhost），外部網路無法直接存取。",
    "about.license.line1": "本軟體遵循 MIT License 開源協議發佈。",
    "about.license.line2": "您可以自由地：",
    "about.license.line3": "  • 將本軟體用於商業用途",
    "about.license.line4": "  • 複製、修改、分發本軟體的全部或部分程式碼",
    "about.license.line5": "  • 在您自己的項目中引用或整合本軟體的程式碼",
    "about.license.line6": "  • 將本軟體作為私有軟體使用，無任何限制",
    "about.license.line7": "唯一要求：",
    "about.license.line8": "  • 在您的項目中保留原作者署名（Pondsi）",
    "about.license.line9": "  • 如果引用了部分程式碼，請在程式碼註釋或文件中註明來源",
    "about.license.line11": "免責聲明：本軟體按「現狀」提供，不作任何明示或暗示的擔保。",
    "about.license.line12": "作者不對使用本軟體所造成的任何損失承擔責任。",
    "about.bugs.line3": "日曆視圖農曆顯示僅支援簡體/繁體中文環境",
    "about.progress.line2": "已完成：任務增刪改查、看板視圖、日曆視圖、統計面板",
    "about.progress.line3": "已完成：小窗模式、系統托盤、快捷鍵、多語言框架",
    "about.progress.line4": "已完成：REST API、資料匯出（JSON/CSV）",
    "about.progress.line5": "開發中：使用者登入與權限系統",
    "about.progress.line6": "計劃中：團隊協作（多人即時同步）",
    "about.progress.line7": "計劃中：資料雲備份與恢復",
    "about.progress.line8": "計劃中：行動端適配（Android/iOS）",
    "about.progress.line9": "計劃中：外掛系統與第三方整合",
    "about.creator.desc": "獨立開發者，專注於桌面效率工具。",
    "about.copyright": "© 2026 Pondsi. All rights reserved.",
    "reminder.dueTime": "截止時間: %s",
    "settings.apiPort": "API 監聽連接埠",
    "settings.apiPortHint": "修改後需重啟應用生效，預設 9527",
    "settings.portLabel": "監聽連接埠:",
    "settings.portHint": "修改後需重啟應用生效，預設 9527",
    "settings.portRange": "連接埠範圍：1024-65535",
    "settings.portSaved": "已儲存，重啟後生效。目前連接埠：%d",
    "settings.portSave": "儲存",
    "settings.apiPortSave": "儲存連接埠",
    "detail.save": "儲存",
    "settings.languageHint": "切換語言後立即生效",
    "common.update": "更新",
    "status.current": "目前: %s",
    "stats.created": "已建立: %s",
    "stats.selectedDate": "選中日期: %s",
    "stats.searchResult": "搜尋: %s（%d 條結果）",
    "about.usage.line9": "日曆視圖：點擊左側「日曆」查看按月分佈的任務",
    "about.usage.line10": "資料匯出：設定頁可匯出 JSON/CSV 格式",
    "settings.memberCount": "共 %d 名成員",
    "settings.memberManage": "選擇要管理（更新/刪除）的成員",
    "settings.updateDelete": "更新/刪除:",
    "settings.deleteMember": "刪除選中成員",
    "settings.deleteConfirm": "確定要刪除成員 %s 嗎？",
    "settings.deleteSelect": "請先選擇要刪除的成員",
    "settings.nameEmpty": "成員名稱不能為空，請先輸入名稱再點「新增」",
    "settings.saveFailed": "儲存失敗: %s",
    "settings.selectAudio": "選擇提示音檔案",
    "settings.audioFiles": "音訊檔案",
    "settings.jsonFiles": "JSON 檔案",
    "settings.csvFiles": "CSV 檔案",
    "settings.soundHint": "預設系統提示音",
    "newTodo.errCreate": "建立失敗：%s",
    "detail.cannotOpen": "無法開啟詳情: %s",
    "detail.loadFailed": "載入詳情失敗",
    "detail.saveFailed": "儲存失敗: %s",
    "detail.toggleFailed": "操作失敗: %s",
    "detail.deleteFailed": "刪除失敗: %s",
    "detail.commentFailed": "傳送失敗: %s",
    "detail.createdAt": "建立: %s | ID: %s",
    "detail.deleteConfirm": "確定刪除任務「%s」？此操作不可撤銷。",
    "detail.deleteTitle": "刪除確認",
    "detail.cancelComplete": "取消完成",
    "detail.unclaim": "取消認領",
    "detail.claimTask": "認領任務",
    "detail.claim": "認領",
    "detail.claimed": "已認領",
    "detail.anonymous": "匿名",
    "detail.unknownUser": "未知使用者",
    "detail.unknown": "未知",
    "detail.commentHint": "輸入評論…",
    "detail.commentSend": "傳送",
    "detail.titlePrefix": "任務詳情 - %s",
    "detail.year": "年",
    "detail.month": "月",
    "detail.day": "日",
    "newTodo.titleLabel": "標題 *",
    "newTodo.titleHint": "要做什麼？",
    "newTodo.descHint": "補充細節（可選）",
    "newTodo.dueDate": "截止日期",
    "newTodo.dueCheck": "設定截止日期",
    "newTodo.errTitle": "請填寫標題",
    "newTodo.errDate": "請選擇完整的年、月、日",
    "newTodo.errDateInvalid": "日期不合法：%s",
    "kanban.add": "＋ 新增",
    "kanban.overdue": "逾期%d天",
    "kanban.left": "剩%d天",
    "kanban.column.pending": "待辦",
    "kanban.column.inProgress": "進行中",
    "kanban.column.done": "已完成",
    "kanban.column.cancelled": "已逾期",
    "mini.overdue": "逾期%d天",
    "mini.left": "剩%d天",
    "countdown.overdue": "逾期%d天",
    "countdown.left": "剩%d天",
    "countdown.daysLeft": "距截止 %d 天",
    "stats.overdueDays": "超時 %d 天",
    "calendar.todoCount": "%d 條待辦",
    "calendar.detailSuffix": " · 待辦 %d 條",
    "calendar.todoUnit": "條待辦",
    "common.items": "條",
    "calendar.noTodos": "這一天沒有待辦事項",
    "shortcut.autoDate": "標題 + 空格 + 日期",
    "shortcut.example1": "例如: 買菜 明天",
    "shortcut.example1desc": "截止日期=明天",
    "shortcut.example2": "例如: 開會 3天後",
    "shortcut.example2desc": "截止日期=3天後",
    "tray.mini": "📋  小窗",
    "tray.open": "🏠  開啟",
    "tray.exit": "❌  退出",
    "view.title.about": "關於",
    "nav.about": "ℹ 關於",
    "about.section.creator": "👨‍💻 製作人",
}

def convert_line(line):
    if not line or line.startswith('#') or '=' not in line:
        return line
    k, v = line.split('=', 1)
    k = k.strip()
    v = v.rstrip('\n')
    if k in OVERRIDES:
        return k + '=' + OVERRIDES[k]
    return k + '=' + zhconv.convert(v, 'zh-tw')

def main():
    src = io.open(BASE + r'\texts_zh.properties', encoding='utf-8')
    lines = src.read().splitlines()
    src.close()
    # 解析 zh 生效值（properties 语义：重复 key 后者覆盖）
    effective = {}
    for line in lines:
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            effective[k.strip()] = v.strip()
    # 按 zh 文件行序输出，重复 key 只输出一次（使用生效值）
    emitted = set()
    out = []
    for line in lines:
        if not line or line.startswith('#') or '=' not in line:
            out.append(line)
            continue
        k = line.split('=', 1)[0].strip()
        if k in emitted:
            continue
        emitted.add(k)
        out.append(k + '=' + OVERRIDES.get(k, zhconv.convert(effective[k], 'zh-tw')))
    with io.open(BASE + r'\texts_zh_tw.properties', 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    missing = set(effective.keys()) - emitted
    print('zh_tw generated, keys:', len(emitted), 'missing:', sorted(missing))

if __name__ == '__main__':
    main()
