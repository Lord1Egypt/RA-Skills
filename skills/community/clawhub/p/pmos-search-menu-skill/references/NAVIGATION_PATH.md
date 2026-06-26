# PMOS 菜单导航完整路径记录

## 已验证的导航路径

### 路径：信息披露 → 实时市场出清节点电价

```
1. 信息披露 (ref=e78)
   ↓
2. 综合查询 (ref=e107) → 打开新标签页
   ↓ [切换到新标签页 F8F567DDB0D0BCAF10B8F288DBA879E3]
   ↓
3. 市场运营 (ref=e50)
   ↓
4. 交易组织及出清 (ref=e591)
   ↓
5. 现货市场申报、出清信息 (ref=e772)
   ↓
6. 实时各节点出清类信息 (ref=e835)
   ↓
7. 实时市场出清节点电价 [待确认位置 - 可能在 iframe 内]
```

## 操作步骤详解

### 步骤 1: 打开网站
```bash
openclaw browser open https://pmos.gs.sgcc.com.cn/
```

### 步骤 2: 等待用户登录
- 用户手动完成登录
- 登录后继续执行

### 步骤 3: 获取页面快照
```bash
openclaw browser snapshot --refs aria --targetId <当前标签页 ID>
```

### 步骤 4: 点击"信息披露"
```bash
openclaw browser act click --ref e78 --targetId <标签页 ID>
```

### 步骤 5: 点击"综合查询"
```bash
openclaw browser act click --ref e107 --targetId <标签页 ID>
```

### 步骤 6: 切换到新标签页
```bash
# 获取标签页列表
openclaw browser tabs

# 切换到包含 "pxf-settlement" 的标签页
openclaw browser focus --targetId F8F567DDB0D0BCAF10B8F288DBA879E3
```

### 步骤 7: 点击"市场运营"
```bash
openclaw browser snapshot --refs aria --targetId F8F567DDB0D0BCAF10B8F288DBA879E3
openclaw browser act click --ref e50 --targetId F8F567DDB0D0BCAF10B8F288DBA879E3
```

### 步骤 8: 点击"交易组织及出清"
```bash
openclaw browser snapshot --refs aria --targetId F8F567DDB0D0BCAF10B8F288DBA879E3
openclaw browser act click --ref e591 --targetId F8F567DDB0D0BCAF10B8F288DBA879E3
```

### 步骤 9: 点击"现货市场申报、出清信息"
```bash
openclaw browser snapshot --refs aria --targetId F8F567DDB0D0BCAF10B8F288DBA879E3
openclaw browser act click --ref e772 --targetId F8F567DDB0D0BCAF10B8F288DBA879E3
```

### 步骤 10: 点击"实时各节点出清类信息"
```bash
openclaw browser snapshot --refs aria --targetId F8F567DDB0D0BCAF10B8F288DBA879E3
openclaw browser act click --ref e835 --targetId F8F567DDB0D0BCAF10B8F288DBA879E3
```

### 步骤 11: 查找"实时市场出清节点电价"
- 可能在左侧菜单树的下一级
- 也可能是页面内的 iframe 内容
- 需要进一步确认位置

## 标签页管理

### 获取标签页列表
```bash
openclaw browser tabs
```

### 切换到指定标签页
```bash
openclaw browser focus --targetId <目标标签页 ID>
```

## 注意事项

1. **登录状态**: 使用前必须先手动登录 PMOS 网站
2. **新标签页**: 点击"综合查询"会打开新标签页，后续操作都在新标签页进行
3. **动态引用**: 页面元素的 aria-ref 可能会变化，每次操作前建议重新获取快照
4. **iframe 内容**: 部分页面内容可能在 iframe 内，需要特殊处理
5. **等待时间**: 菜单展开和页面加载需要时间，建议操作间添加适当延迟

## 故障排除

### 问题：找不到菜单项引用
**解决**: 重新执行 `browser snapshot` 获取最新引用

### 问题：点击后无反应
**解决**: 检查是否在新标签页操作，使用 `browser focus` 切换

### 问题：菜单未展开
**解决**: 点击父菜单后等待 2-3 秒再获取快照

## 实际执行记录 (2026-03-17)

### 已确认的元素引用
| 菜单项 | 引用 ID | 备注 |
|--------|--------|------|
| 信息披露 | e78 | 主标签页 |
| 综合查询 | e107 | 打开新标签页 |
| 市场运营 | e50 | 新标签页内顶部菜单 |
| 交易组织及出清 | e591 | 左侧树形菜单 |
| 现货市场申报、出清信息 | e772 | 左侧树形菜单 |
| 实时各节点出清类信息 | e835 | 左侧树形菜单 |
| 实时市场出清节点电价 | 待确认 | 可能在 iframe 内 |

### 标签页信息
- 主标签页 ID: `E9F26CE87D84E86FA63D07C52515A404`
- 综合查询标签页 ID: `F8F567DDB0D0BCAF10B8F288DBA879E3`
- 综合查询标签页 URL: `https://pmos.gs.sgcc.com.cn/pxf-settlement-outnetpub/#/pxf-settlement-outnetpub/columnHomeLeftMenuNew`
