# Knowledge Orchestrator 鎶€鑳?
**鐗堟湰锛?* v0.1  
**鍒涘缓鏃堕棿锛?* 2026 骞?3 鏈?26 鏃? 
**鐘舵€侊細** 馃攧 寮€鍙戜腑

---

## 馃幆 鍔熻兘

- 鉁?缁熶竴鎼滅储锛圸otero + Obsidian + IMA锛?- 鈴?鍚屾鍒?IMA
- 鈴?鏂囩尞 - 绗旇鍏宠仈
- 鈴?鐭ヨ瘑鍥捐氨

---

## 馃殌 蹇€熷紑濮?
### 閰嶇疆鍑瘉

**Zotero:**
```bash
mkdir -p D:\Personal\OpenClaw\.config\zotero
echo "your_zotero_api_key" > D:\Personal\OpenClaw\.config\zotero\api_key
```

**IMA:**
```bash
# 宸查厤缃湪 D:\Personal\OpenClaw\.config\ima\
# client_id 鍜?api_key 宸插瓨鍦?```

### 缁熶竴鎼滅储

```bash
cd skills/knowledge-orchestrator
python knowledge_search.py -q "RTHS" --all
```

---

## 馃摉 浣跨敤绀轰緥

### 鎼滅储鎵€鏈夊钩鍙?
```bash
python knowledge_search.py -q "鎸姩鍙版帶鍒? --all -l 10
```

### 浠呮悳绱?Obsidian

```bash
python knowledge_search.py -q "RTHS" --obsidian
```

### 鍚屾绗旇鍒?IMA锛堝緟寮€鍙戯級

```bash
python knowledge_sync.py --note "鎸姩鍙版帶鍒剁郴缁熸灦鏋? --to-ima
```

---

## 馃搧 鏂囦欢缁撴瀯

```
skills/knowledge-orchestrator/
鈹溾攢鈹€ SKILL.md                 # 鎶€鑳藉畾涔?鈹溾攢鈹€ README.md                # 浣跨敤璇存槑锛堟湰鏂囦欢锛?鈹溾攢鈹€ knowledge_search.py      # 缁熶竴鎼滅储
鈹溾攢鈹€ knowledge_sync.py        # 鍚屾鍒?IMA锛堝緟寮€鍙戯級
鈹溾攢鈹€ knowledge_link.py        # 鏂囩尞 - 绗旇鍏宠仈锛堝緟寮€鍙戯級
鈹斺攢鈹€ knowledge_graph.py       # 鐭ヨ瘑鍥捐氨锛堝緟寮€鍙戯級
```

---

## 馃攧 宸ヤ綔娴佺▼

### 鏂囩尞绠＄悊宸ヤ綔娴?```
1. Zotero 瀵煎叆鏂囩尞
   鈫?2. Obsidian 鍒涘缓绗旇
   鈫?3. 鍗忚皟鍣ㄨ嚜鍔ㄥ叧鑱?   鈫?4. 鍚屾鍒?IMA 浜戠
```

### 鐭ヨ瘑妫€绱㈠伐浣滄祦
```
鐢ㄦ埛鎼滅储 鈫?鍗忚皟鍣ㄦ悳绱笁骞冲彴 鈫?姹囨€昏繑鍥炵粨鏋?```

---

## 馃搳 骞冲彴瀵规瘮

| 骞冲彴 | 鐢ㄩ€?| 鎼滅储鑼冨洿 | 鍚屾鏂瑰悜 |
|------|------|----------|----------|
| **Zotero** | 鏂囩尞绠＄悊 | 鏂囩尞鍏冩暟鎹?| 鍗曞悜锛堝鍏ワ級 |
| **Obsidian** | 鐭ヨ瘑绗旇 | 鏈湴绗旇 | 鍙屽悜 |
| **IMA** | 浜戠鍗忎綔 | 浜戠绗旇 | 鍗曞悜锛堝鍑猴級 |

---

## 馃敡 寰呭紑鍙戝姛鑳?
- [ ] `knowledge_sync.py` - 鍚屾鍒?IMA
  - 閫夋嫨绗旇鍚屾
  - 鑷姩鍚屾瑙勫垯
  - 鍐茬獊澶勭悊

- [ ] `knowledge_link.py` - 鏂囩尞 - 绗旇鍏宠仈
  - 閫氳繃 DOI 鍏宠仈
  - 鍙屽悜閾炬帴缁存姢

- [ ] `knowledge_graph.py` - 鐭ヨ瘑鍥捐氨
  - 鍙鍖栧睍绀?  - 缁熻鍒嗘瀽

- [ ] IMA API 闆嗘垚
  - 绗旇涓婁紶
  - 浜戠鎼滅储

---

## 馃挕 鏈€浣冲疄璺?
### 鎼滅储鎶€宸?- 浣跨敤鍏蜂綋鍏抽敭璇嶏紙濡?RTHS"鑰岄潪"璇曢獙"锛?- 闄愬埗缁撴灉鏁伴噺锛?l 5锛夋彁楂橀€熷害
- 瀹氭湡娓呯悊鏃犵敤绗旇

### 鍚屾绛栫暐
- 浠呭悓姝ラ噸瑕佺瑪璁板埌 IMA
- 瀹氭湡澶囦唤 Obsidian 浠撳簱
- 鏂囩尞鍏冩暟鎹互 Zotero 涓哄噯

---

## 馃摓 闂鍙嶉

閬囧埌闂璇锋鏌ワ細
1. Zotero API Key 鏄惁閰嶇疆
2. IMA 鍑瘉鏄惁鏈夋晥
3. research 鐩綍鏄惁瀛樺湪

---

**鐭ヨ瘑绠＄悊鎶€鑳界郴缁熷紑鍙戝畬鎴愶紒** 馃帀

涓嬩竴姝ワ細
- 娴嬭瘯涓変釜鎶€鑳?- 閰嶇疆鍑瘉
- 寮€濮嬩娇鐢?
