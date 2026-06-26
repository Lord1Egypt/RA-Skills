# 保险费率二维表生成工具

## 快速开始

### 方式一：命令行运行

```bash
# 生成默认参数的费率表
node scripts/generate-rate-table.js "星海赢家朱雀版"

# 或使用 bash 脚本
chmod +x scripts/generate-rate-table.sh
./scripts/generate-rate-table.sh "星海赢家朱雀版"
```

### 方式二：手动执行 Node 代码

```javascript
const XLSX = require('xlsx');

const plans = ['计划一', '计划二'];
const paymentYears = ['趸交', '10年', '20年'];
const paymentMethods = ['一次交清', '月交', '年交', '半年交', '季交', '不定期交'];
const receiveAges = ['自55周岁', '自60周岁'];
const genders = ['女', '男'];
const ages = Array.from({length: 71}, (_, i) => i);

// 生成有效列组合（符合约束规则）
const cols = [];
plans.forEach(plan => {
  paymentYears.forEach(py => {
    paymentMethods.forEach(pm => {
      // 约束规则
      if (pm === '一次交清' && py !== '趸交') return;
      if (pm !== '一次交清' && py === '趸交') return;
      
      receiveAges.forEach(ra => {
        genders.forEach(gender => {
          cols.push({plan, py, pm, ra, gender});
        });
      });
    });
  });
});

// 生成数据
const data = [];
data.push(['保障计划', ...cols.map(c => c.plan)]);
data.push(['交费期间', ...cols.map(c => c.py)]);
data.push(['交费方式', ...cols.map(c => c.pm)]);
data.push(['领取时间', ...cols.map(c => c.ra)]);
data.push(['被保人年龄/被保人性别', ...cols.map(c => c.gender)]);

ages.forEach(age => {
  data.push([age, ...cols.map((c, i) => 34000 + age + i)]); // 示例费率
});

// 保存文件
const wb = XLSX.utils.book_new();
const ws = XLSX.utils.aoa_to_sheet(data);
ws['!cols'] = [{wch: 18}, ...cols.map(() => ({wch: 10}))];
XLSX.utils.book_append_sheet(wb, ws, '费率表');
XLSX.writeFile(wb, '费率表.xlsx');
```

## 参数配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 产品名称 | 文件名使用 | 费率表 |
| plans | 保障计划 | 计划一,计划二 |
| payment-years | 交费期间 | 趸交,10年,20年 |
| payment-methods | 交费方式 | 一次交清,月交,年交,半年交,季交,不定期交 |
| receive-ages | 领取时间 | 自55周岁,自60周岁 |
| age-range | 年龄范围 | 0-70 |

## 依赖

- Node.js
- xlsx 包：`npm install xlsx`
