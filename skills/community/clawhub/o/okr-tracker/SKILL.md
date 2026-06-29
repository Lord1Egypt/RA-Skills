---
name: OKR杩涘害杩借釜澶у笀
slug: okr-tracker
description: >
  浼佷笟绾KR鐩爣涓庡叧閿粨鏋滆嚜鍔ㄨ拷韪妧鑳姐€傛敮鎸佷粠Notion/Jira/椋炰功/Lark/Google Sheets绛夊骞冲彴鍚屾OKR鏁版嵁锛?  鑷姩璁＄畻杩涘害鐧惧垎姣斻€侀娴嬭揪鎴愰闄┿€佺敓鎴愬懆/鏈?瀛ｅ害OKR鍋ュ悍鎶ュ憡锛屾彁渚涘亸绂婚璀﹀拰鏀硅繘寤鸿銆?  鏀寔OKR灞傜骇瀵归綈妫€鏌ャ€佽法閮ㄩ棬渚濊禆鍒嗘瀽銆佸巻鍙茶秼鍔垮姣斻€?version: 1.0.0
author: ai-gaoqian
tags:
  - okr
  - goal-tracking
  - project-management
  - enterprise
  - performance-management
  - team-productivity
  - data-sync
metadata:
  openclaw:
    requires:
      python: ">=3.10"
      packages:
        - pandas>=2.0.0
        - matplotlib>=3.7.0
        - requests>=2.28.0
      api_keys:
        - optional: NOTION_API_KEY
        - optional: JIRA_API_TOKEN
        - optional: FEISHU_APP_TOKEN
      memory: 256MB
      cpu: 0.3
    pricing:
      model: per-use
      currency: CNY
      amount: 0.50
      payment_method: alipay_ai_receipt
---

# OKR杩涘害杩借釜澶у笀 (OKR Tracker)

## 姒傝堪
OKR杩涘害杩借釜澶у笀涓轰紒涓氬洟闃熸彁渚涘叏闈㈢殑鐩爣涓庡叧閿粨鏋滆嚜鍔ㄨ拷韪兘鍔涳紝甯姪绠＄悊鑰呭疄鏃舵帉鎻KR鎵ц鐘舵€侊紝鍙婃椂鍙戠幇椋庨櫓骞跺仛鍑鸿皟鏁淬€?
## 鏍稿績鍔熻兘

### 1. 澶氭簮鏁版嵁鍚屾
鏀寔浠庝互涓嬪钩鍙拌嚜鍔ㄥ悓姝KR鏁版嵁锛?- Notion锛堥€氳繃Notion API锛?- Jira锛堥€氳繃Jira REST API锛?- 椋炰功/Lark锛堥€氳繃椋炰功寮€鏀惧钩鍙癆PI锛?- Google Sheets锛堥€氳繃Google Sheets API锛?- 鏈湴CSV/Excel鏂囦欢瀵煎叆

### 2. 杩涘害鑷姩璁＄畻
- 鍩轰簬瀛愪换鍔″畬鎴愬害鑷姩璁＄畻KR杩涘害
- 鍔犳潈鑱氬悎澶氫釜KR璁＄畻O鐨勮揪鎴愮巼
- 鏃堕棿杩涘害 vs 鐩爣杩涘害鐨勫亸宸垎鏋?- 鍩轰簬鍘嗗彶瓒嬪娍鐨勫畬鎴愭椂闂撮娴?
### 3. 鏅鸿兘棰勮
- 杩涘害婊炲悗鑷姩鏍囪锛堥粍鑹查璀︼細鍋忓樊>10%锛岀孩鑹查璀︼細鍋忓樊>30%锛?- 鍩轰簬褰撳墠閫熷害棰勬祴瀛ｅ害鏈揪鎴愭鐜?- 鍏抽敭璺緞琚樆濉炵殑渚濊禆椤硅嚜鍔ㄥ憡璀?- 闀挎湡鏃犳洿鏂扮殑OKR浼戠湢鎻愰啋

### 4. 鎶ュ憡鐢熸垚
- 姣忔棩OKR蹇収
- 鍛ㄥ害OKR鍋ュ悍鎶ュ憡锛堝惈鍥㈤槦鍜屼釜浜虹淮搴︼級
- 鏈堝害瓒嬪娍鍒嗘瀽锛堢幆姣?鍚屾瘮锛?- 瀛ｅ害OKR澶嶇洏鎶ュ憡锛堝惈杈炬垚鐜囥€佸叧閿噷绋嬬鍥為【锛?
### 5. OKR璐ㄩ噺瀹¤
- OKR瀵归綈妫€鏌ワ細涓汉O鏄惁鏀拺鍥㈤槦O
- KR鍙　閲忔€ц瘎鍒?- 璺ㄩ儴闂ㄤ緷璧栧叧绯诲彲瑙嗗寲
- OKR鏁伴噺鍚堢悊鎬у缓璁?
## 浣跨敤鏂瑰紡
```
clawhub install okr-tracker
```

## 鍏稿瀷鍛戒护
```
璇风敓鎴愭湰鍛∣KR鍋ュ悍鎶ュ憡
璇锋鏌ユ垜鐨凮KR瀵归綈鎯呭喌
璇峰垎鏋愬洟闃烸2 OKR鐨勮揪鎴愰闄?璇烽娴嬫湰鏈圤KR鏈€缁堝畬鎴愮巼
```

## 杈撳嚭绀轰緥
```
馃搳 鏈懆OKR鍋ュ悍鎶ュ憡 (2026-W24)

鎬讳綋鍋ュ悍搴? 馃煛 鑹ソ (72%)
鎬籓KR鏁? 8 | 杈炬爣: 4 | 椋庨櫓: 2 | 婊炲悗: 2

鈿狅笍 椋庨櫓椤?
1. [O2] 鐢ㄦ埛澧為暱鐩爣 - 杈炬垚鐜囦粎45% (鏃堕棿宸茶繃67%)
   鈫?寤鸿: KR2.1銆屾棩娲绘彁鍗囥€嶄弗閲嶆粸鍚庯紝闇€杩藉姞璧勬簮
2. [O3] 浜у搧涓婄嚎閲岀▼纰?- 渚濊禆椤广€屽悗绔疉PI寮€鍙戙€嶅凡闃诲5澶?   鈫?寤鸿: 鍗忚皟鍚庣鍥㈤槦浼樺厛鎺掓湡

馃搱 瓒嬪娍: 鏈懆鐜瘮涓婂崌8%锛岄璁″搴︽湯杈炬垚鐜?2-85%
```

## 瀹夊叏涓庨殣绉?- 鏁版嵁浠呭湪鏈湴澶勭悊锛屼笉涓婁紶鑷崇涓夋柟
- API瀵嗛挜閫氳繃鐜鍙橀噺瀹夊叏绠＄悊
- 鏀寔鏁版嵁鑴辨晱鍐嶅鍑?- 鎶ュ憡鍙厤缃闂潈闄?