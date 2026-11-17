# 撮合台业务场景手册

## 三种身份，三种用法

### A. 我做中间人（撮合方）

欧洲客户要找中国代工厂，两边都是我的资源。撮合方视角：

```bash
# 1. 双方都登记为主体（我方标 --self）
publish.py party --name "Dipperson Medical" --side both --country 中国 --self --email ... --user U001
publish.py party --name "NordImplant GmbH"  --side buyer --country 德国 --person "Klaus Weber" --email ... --user U001
publish.py party --name "华康精密制造"       --side seller --country 中国 --person "李四" --email ... --user U001

# 2. 分别发布需求与能力
publish.py demand     --party P002 --title "PEEK脊柱融合器代工" --desc "..." --user U001
publish.py capability --party P003 --title "脊柱植入物PEEK加工" --desc "..." --user U001

# 3. 撮合
match.py run --all --user U001 --verbose

# 4. 分别向两边确认意向，双方都点头后交换
intro.py request --match M001 --side buyer  --user U001 --note "买方有意向，想看产线"
intro.py accept  --match M001 --side seller --user U001 --note "卖方可以接"
intro.py reveal  --match M001 --user U001

# 5. 把联系方式分别转给两边，回写结果
intro.py feedback --match M001 --user U001 --result "双方已直接联系，寄样中"
```

撮合方能看到所有 connected 的联系方式——这是设计内的，不然没法搭接。

### B. 我自己要找供应商（买方视角）

```bash
publish.py demand --party P001 --title "找钛合金锁定板OEM" \
  --desc "Ti6Al4V锁定接骨板，12000套/年，需ISO13485+FDA注册，美国市场" \
  --qty "12000套/年" --deadline 2027-09-30 --user U001

# 先看看现有池子里有没有
match.py run --demand D002 --user U001 --min-score 40

# 没有就从展会名录找线索
import_expo.py --country 中国 --kw "trauma" --limit 50 --user U001
match.py leads --demand D002 --user U001

# 看中某家 → 激活 → 发能力 → 再撮合
publish.py activate --lead P0xx --person "王五" --email ... --user U001
```

### C. 我要推销产能（卖方视角）

```bash
publish.py capability --party P001 --title "创伤与脊柱植入物代工" \
  --desc "CNC加工钛合金与PEEK，阳极氧化、EO灭菌、洁净包装，ISO13485，出口欧盟与美国" \
  --capacity "3万件/月" --moq "500件" --lead-time "40天" --user U001

# 反向撮合：看池子里谁在找我能做的
match.py run --capability C001 --user U001 --min-score 40
```

## 状态机

```
                    ┌─ decline ─→ declined（作废，可 --block 永久拉黑）
                    │
suggested ─accept─→ half ─accept─→ connected ─reveal─→ 已交换联系方式
  待确认          单方已同意        双方同意        （消耗 8/日 配额）
                    │
                    └─ 另一方 decline ─→ declined
```

- `request` 会让发起方自动同意自己那一侧
- 只有 `connected` 状态才能 `reveal`
- `declined` 不可恢复（需要的话重新跑 match 生成新记录）

## 撮合分怎么读

| 分数 | 含义 | 建议 |
|---|---|---|
| 70+ | 高度契合 | 直接推进 |
| 50-69 | 有戏，看缺口 | 先补缺口再谈 |
| 40-49 | 勉强 | 降低门槛看一眼再说 |
| <40 | 不建议 | 默认不入库 |

**先看缺口，再看分数。** 一个 57 分但写着「资质缺口：对方尚无 CE MDR」的撮合，
比一个 63 分但资质全对的撮合更值得关注——前者告诉你差在哪，可能是个可以补的机会。

## 反骚扰红线（守则七条）

1. 发布的信息真实准确，不虚构需求试探行情、不夸大产能资质
2. 只通过撮合台接触对方，不绕过流程私下找上门
3. 对方拒绝或长时间未回应后，不再重复接触、不换渠道纠缠
4. 不把撮合得到的联系方式转售、外传、公开张贴或导入群发系统
5. 每次沟通表明真实身份与来意，留下可回拨的联系方式
6. 涉及图纸、报价、工艺参数，先签 NDA 再交换
7. 接受全程留痕、可追溯到个人

## 出问题怎么办

| 情况 | 处理 |
|---|---|
| 对方说别再联系 | `intro.py decline --match M00x --side seller --block` 或 `core.py block --company "..."` |
| 误拉黑了 | `core.py unblock --company "..."` |
| 怀疑有人批量抓 | `core.py audit --tail 50` 看消耗；配额本身就是限速 |
| 担心记录被改 | `core.py audit --verify`，改一条全链断 |
| 数据乱了重来 | `init_db.py --reset` 然后 `demo.py --yes` |
| 撮合总匹配不上 | 检查描述是否触发词典；用 `--cat/--material/--cert` 手动指定 |

## 备案：对外发布前要补的

当前是内部工具。若要作为技能对外发布，需补：

- 敏感扫描（示例数据里的 example 邮箱要清理）
- LICENSE 文件与正文版权段
- 权属证明五件套（著作权/知识版权声明/免责声明/时间戳/指纹）
- 安全稳定性测试 + 多维度雷达图
- 演示数据脱敏（现在是虚构公司名 + example.com，本身安全）
