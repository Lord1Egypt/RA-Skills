# Poe.ninja API 技能包

Path of Exile 市場價格查詢工具，透過 poe.ninja API 獲取遊戲物品即時價格資料。

## 功能特色

- 🔍 **通貨查詢** - 查詢 Chaos、Divine、Mirror 等通貨匯率
- 📦 **物品查詢** - 支援 29 種物品類型（裝備、技能寶石、地圖等）
- 🔎 **跨類型搜尋** - 一次搜尋所有物品類型
- 📊 **價格趨勢** - 顯示價格變化百分比

## 安裝方式

### 方法一：直接安裝 .skill 檔案

下載 `poe-ninja-api.skill` 檔案，放入你的技能目錄：

```bash
# macOS
cp poe-ninja-api.skill ~/.qclaw/skills/

# 解壓縮
cd ~/.qclaw/skills
unzip poe-ninja-api.skill
```

### 方法二：從原始碼安裝

```bash
git clone https://github.com/qpooqp77/poe-ninja-api.git
cd poe-ninja-api
```

## 使用方式

### 在 QClaw/OpenClaw 中使用

安裝後，可以直接用自然語言查詢：

- 「查 Divine Orb 價格」
- 「查 Mageblood 多少錢」
- 「搜尋 Mirror 相關物品」

### 命令列使用

#### 查詢通貨價格

```bash
python scripts/get_currency.py --league Settlers
python scripts/get_currency.py --league Standard --search "divine"
```

#### 查詢物品價格

```bash
python scripts/get_item.py --league Settlers --type UniqueWeapon
python scripts/get_item.py --league Standard --type SkillGem --search "Enlighten"
```

#### 跨類型搜尋

```bash
python scripts/search_item.py --league Standard --query "Mirror"
python scripts/search_item.py --league Standard --query "Mageblood" --min-price 1000
```

## 支援的物品類型

### 通貨類（currencyoverview）

| 類型 | 說明 |
|------|------|
| Currency | 通貨（Chaos、Divine、Mirror 等） |
| Fragment | 碎片 |

### 物品類（itemoverview）

| 類型 | 說明 |
|------|------|
| Oil | 油 |
| Incubator | 孵化器 |
| Scarab | 聖甲蟲 |
| Fossil | 化石 |
| Resonator | 共振器 |
| Essence | 精髓 |
| DivinationCard | 預言卡 |
| SkillGem | 技能寶石 |
| BaseType | 基底類型 |
| HelmetEnchant | 頭盔附魔 |
| UniqueMap | 傳奇地圖 |
| Map | 地圖 |
| UniqueJewel | 傳奇珠寶 |
| UniqueFlask | 傳奇藥水 |
| UniqueWeapon | 傳奇武器 |
| UniqueArmour | 傳奇護甲 |
| UniqueAccessory | 傳奇飾品 |
| Beast | 野獸 |
| Vial | 小瓶 |
| DeliriumOrb | 譫妄球 |
| Omen | 徵兆 |
| UniqueRelic | 傳奇遺物 |
| ClusterJewel | 叢集珠寶 |
| BlightedMap | 凋零地圖 |
| BlightRavagedMap | 凋零掠奪地圖 |
| Invitation | 邀請函 |
| Memory | 記憶 |
| Coffin | 棺材 |
| AllflameEmber | 全燃餘燼 |

## API 來源

本工具使用 [poe.ninja](https://poe.ninja) 提供的公開 API。

- API 文件參考：[ayberkgezer/poe.ninja-API-Document](https://github.com/ayberkgezer/poe.ninja-API-Document)

## 注意事項

1. **聯盟名稱** - 每個新賽季聯盟名稱不同，需使用當前聯盟名稱
2. **價格更新** - poe.ninja 資料每小時更新一次
3. **低置信度資料** - 交易量低時價格可能不準確
4. **請求頻率** - 請避免短時間內大量請求

## 授權

MIT License

## 作者

Created for QClaw/OpenClaw
