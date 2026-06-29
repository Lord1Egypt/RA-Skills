---
name: PostgreSQL鏌ヨ浼樺寲椤鹃棶
slug: postgres-optimizer
description: >
  AI椹卞姩鐨凱ostgreSQL鏌ヨ鎬ц兘浼樺寲鎶€鑳姐€傚垎鏋愭參鏌ヨ鏃ュ織銆佹墽琛岃鍒?EXPLAIN ANALYZE)銆佺储寮曠瓥鐣ャ€?  琛ㄧ粨鏋勫拰缁熻淇℃伅锛屾彁渚涘叿浣撶殑浼樺寲寤鸿鍜屽彲鐩存帴鎵ц鐨凷QL DDL/DML銆?  瑕嗙洊绱㈠紩浼樺寲銆佹煡璇㈤噸鍐欍€佸垎鍖虹瓥鐣ャ€乂ACUUM璋冧紭銆佽繛鎺ユ睜閰嶇疆绛夊叏缁村害浼樺寲銆?  鏀寔PostgreSQL 12-17鎵€鏈夌増鏈€?version: 1.0.0
author: ai-gaoqian
tags:
  - postgresql
  - database
  - performance
  - sql-optimization
  - query-tuning
  - devops
  - dba
metadata:
  openclaw:
    requires:
      python: ">=3.10"
      packages:
        - psycopg2-binary>=2.9.0
        - sqlparse>=0.4.0
        - pandas>=2.0.0
      api_keys: []
      memory: 256MB
      cpu: 0.3
    pricing:
      model: per-use
      currency: CNY
      amount: 0.50
      payment_method: alipay_ai_receipt
---

# PostgreSQL鏌ヨ浼樺寲椤鹃棶 (Postgres Optimizer)

## 姒傝堪
PostgreSQL鏌ヨ浼樺寲椤鹃棶鏄潰鍚戝紑鍙戣€呭拰DBA鐨勬櫤鑳芥暟鎹簱鎬ц兘浼樺寲鎶€鑳斤紝鑳藉娣卞害鍒嗘瀽PostgreSQL鏌ヨ鎬ц兘鐡堕锛屾彁渚涚簿鍑嗙殑浼樺寲鏂规鍜屼竴閿彲鎵ц鐨凷QL鑴氭湰銆?
## 鏍稿績鍔熻兘

### 1. 鎱㈡煡璇㈠垎鏋?- 瑙ｆ瀽pg_stat_statements鍜屾參鏌ヨ鏃ュ織
- 璇嗗埆Top N鎱㈡煡璇㈠苟鎸夊奖鍝嶆帓搴?- 鎵ц璁″垝鍙鍖栬В璇?- 鎴愭湰浼扮畻鍋忓樊妫€娴嬶紙璁″垝琛屾暟 vs 瀹為檯琛屾暟锛?- 涓存椂鏂囦欢浣跨敤寮傚父鍛婅

### 2. 绱㈠紩绛栫暐浼樺寲
- 缂哄け绱㈠紩鑷姩妫€娴嬪拰鎺ㄨ崘
- 鍐椾綑/鏈娇鐢ㄧ储寮曡瘑鍒?- 閮ㄥ垎绱㈠紩(Partial Index)寤鸿
- 琛ㄨ揪寮忕储寮?Expression Index)鎺ㄨ崘
- 瑕嗙洊绱㈠紩(Covering Index)鍒嗘瀽
- BRIN/GIN/GiST绱㈠紩绫诲瀷鎺ㄨ崘
- 绱㈠紩鑶ㄨ儉妫€娴嬪拰REINDEX寤鸿

### 3. 鏌ヨ閲嶅啓浼樺寲
- 瀛愭煡璇紭鍖栵紙杞琂OIN/CTE/LATERAL锛?- JOIN椤哄簭鍜岀被鍨嬩紭鍖栧缓璁?- WHERE瀛愬彞閫夋嫨鎬у垎鏋?- LIMIT+OFFSET鍒嗛〉浼樺寲锛圞eyset Pagination鎺ㄨ崘锛?- OR鏉′欢杞琔NION ALL浼樺寲
- 鑱氬悎鏌ヨ浼樺寲锛團ILTER瀛愬彞鎺ㄨ崘锛?- 绐楀彛鍑芥暟鎬ц兘鍒嗘瀽

### 4. 琛ㄧ粨鏋勪紭鍖?- 鏁版嵁绫诲瀷浼樺寲锛堥伩鍏嶄笉蹇呰鐨則ext/bigint锛?- 琛ㄥ垎鍖虹瓥鐣ュ缓璁紙RANGE/LIST/HASH锛?- 瑙勮寖鍖?vs 鍙嶈鑼冨寲鏉冭　鍒嗘瀽
- 澶ц〃鍨傜洿/姘村钩鎷嗗垎寤鸿
- TOAST绛栫暐璇勪及

### 5. 閰嶇疆璋冧紭
- shared_buffers / work_mem / effective_cache_size 寤鸿
- autovacuum鍙傛暟璋冧紭
- max_parallel_workers 骞惰搴﹀缓璁?- WAL閰嶇疆浼樺寲
- 杩炴帴姹?max_connections)璇勪及

### 6. 缁熻淇℃伅绠＄悊
- 琛ㄧ粺璁′俊鎭柊椴滃害妫€鏌?- n_distinct / MCV鍊煎紓甯稿憡璀?- 鎵╁睍缁熻(CREATE STATISTICS)寤鸿
- ANALYZE绛栫暐浼樺寲

## 浣跨敤鏂瑰紡
```
clawhub install postgres-optimizer
```

## 鍏稿瀷鍛戒护
```
璇峰垎鏋愭垜鐨勬參鏌ヨ鏃ュ織鏂囦欢
璇峰杩欎釜SQL杩涜浼樺寲鍒嗘瀽锛歋ELECT ...
璇锋鏌ユ垜鐨勭储寮曠瓥鐣ユ槸鍚﹀悎鐞?璇蜂负浠ヤ笅琛ㄧ粨鏋勬彁渚涗紭鍖栧缓璁?璇疯瘖鏂璓ostgreSQL瀹炰緥鐨勬暣浣撴€ц兘鐡堕
```

## 杈撳嚭绀轰緥
```
馃攳 PostgreSQL鏌ヨ浼樺寲鎶ュ憡

鏌ヨ: SELECT o.*, u.name FROM orders o JOIN users u ON o.user_id = u.id WHERE o.created_at > '2026-01-01' AND o.status = 'pending' ORDER BY o.created_at DESC LIMIT 100;

褰撳墠鎬ц兘:
  鎵ц鏃堕棿: 2,847ms | 鎵弿琛屾暟: 1,250,000 | 浣跨敤涓存椂鏂囦欢: 鏄?
馃幆 闂璇婃柇:
1. [涓ラ噸] orders琛ㄧ己灏?created_at, status)澶嶅悎绱㈠紩
   鈫?褰撳墠鍏ㄨ〃鎵弿1,250,000琛?2. [涓瓑] users琛↗OIN鍒梚d缂哄皯绱㈠紩锛堝鏈夊垯蹇界暐锛?3. [杞诲井] ORDER BY + LIMIT鍙紭鍖栦负绱㈠紩鎵弿

鉁?鎺ㄨ崘浼樺寲鏂规:
```sql
-- 1. 鍒涘缓鏍稿績澶嶅悎绱㈠紩锛堥璁℃彁鍗?5%锛?CREATE INDEX idx_orders_created_status ON orders(created_at DESC, status) WHERE status = 'pending';

-- 2. 浼樺寲鍚庣殑鏌ヨ锛堟棤闇€鏀瑰姩锛岀储寮曚細鑷姩鐢熸晥锛?-- 棰勮鎵ц鏃堕棿: <50ms | 鎵弿琛屾暟: ~100
```

馃搳 棰勪及浼樺寲鏁堟灉:
  鎵ц鏃堕棿: 2,847ms 鈫?<50ms (98%鎻愬崌)
  鎵弿琛屾暟: 1,250,000 鈫?~100
  鍐呭瓨浣跨敤: 鏄捐憲闄嶄綆
```

## 瀹夊叏涓庨殣绉?- 浠呰鍙栨暟鎹簱鍏冩暟鎹拰鎵ц璁″垝锛屼笉淇敼鏁版嵁
- 鎵€鏈夊缓璁甋QL閮戒細鏄庣‘鏍囨敞椋庨櫓绛夌骇
- 鏀寔鍙鐢ㄦ埛鏉冮檺杩愯
- 涓嶈褰曟垨澶栦紶鏌ヨ鍐呭鍜屾暟鎹簱缁撴瀯
- 鐢熶骇鐜鎿嶄綔鍓嶉渶鐢ㄦ埛纭
