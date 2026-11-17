# 详细参考 - html-coder-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
class WCAGComplianceChecker:
    """WCAG 2.1 AA/AAA 合规检查器"""

    def __init__(self, level="AA"):
        self.level = level
        self.violations = []

    def check_full_compliance(self, html_content):
        """全面合规检查"""
        checks = {
            "1.1.1": self._check_non_text_content,    # 非文本内容
            "1.3.1": self._check_info_relationship,   # 信息与关系
            "1.4.3": self._check_color_contrast,      # 对比度
            "1.4.4": self._check_text_resize,         # 文本缩放
            "2.1.1": self._check_keyboard_accessible,  # 键盘可访问
            "2.4.1": self._check_skip_navigation,     # 跳过导航
            "2.4.2": self._check_page_titled,         # 页面标题
            "2.4.4": self._check_link_purpose,        # 链接目的
            "3.1.1": self._check_lang_attribute,      # 语言属性
            "3.3.2": self._check_labels_instructions,  # 标签与说明
            "4.1.1": self._check_html_valid,          # HTML有效
            "4.1.2": self._check_name_role_value,     # 名称角色值
        }

        for rule_id, check_func in checks.items():
            violations = check_func(html_content)
            self.violations.extend(violations)

        return self._generate_report()

    def _check_non_text_content(self, html):
        violations = []
        if '<img' in html and 'alt=' not in html:
            violations.append({
                "rule": "1.1.1 (A)",
                "severity": "critical",
                "message": "图片缺少 alt 属性",
                "fix": "为所有 img 添加 alt 描述文本"
            })
        return violations

    def _check_info_relationship(self, html):
        violations = []
        if '<table>' in html and '<th' not in html:
            violations.append({
                "rule": "1.3.1 (A)",
                "severity": "serious",
                "message": "表格缺少表头单元格 (th)",
                "fix": "使用 th 标签标记表头"
            })
        return violations

    def _check_color_contrast(self, html):
        return [{
            "rule": "1.4.3 (AA)",
            "severity": "serious",
            "message": "需验证文本对比度 ≥ 4.5:1",
            "fix": "使用对比度检查工具验证所有文本"
        }]

    def _check_keyboard_accessible(self, html):
        violations = []
        if 'onclick' in html and 'onkeydown' not in html and 'onkeypress' not in html:
            violations.append({
                "rule": "2.1.1 (A)",
                "severity": "critical",
                "message": "鼠标事件缺少键盘等价处理",
                "fix": "为 onclick 添加 onkeydown 等价处理"
            })
        return violations

    def _check_skip_navigation(self, html):
        if 'skip' not in html.lower():
            return [{
                "rule": "2.4.1 (A)",
                "severity": "moderate",
                "message": "缺少跳过导航链接",
                "fix": "添加 <a href='#main'>跳到主内容</a>"
            }]
        return []

    def _check_page_titled(self, html):
        if '<title>' not in html:
            return [{
                "rule": "2.4.2 (A)",
                "severity": "serious",
                "message": "页面缺少 title 标签",
                "fix": "添加描述性的 <title> 标签"
            }]
        return []

    def _check_lang_attribute(self, html):
        if 'lang=' not in html.split('<html')[1].split('>')[0]:
            return [{
                "rule": "3.1.1 (A)",
                "severity": "serious",
                "message": "html 标签缺少 lang 属性",
                "fix": "添加 lang='zh-CN' 等语言属性"
            }]
        return []

    def _check_labels_instructions(self, html):
        violations = []
        if '<input' in html and '<label' not in html and 'aria-label' not in html:
            violations.append({
                "rule": "3.3.2 (A)",
                "severity": "critical",
                "message": "表单输入缺少关联标签",
                "fix": "使用 <label> 或 aria-label 关联输入"
            })
        return violations

    def _check_html_valid(self, html):
        return []  # 实际实现会检查HTML有效性
    def _check_name_role_value(self, html):
        return []  # 实际实现会检查ARIA属性
    def _generate_report(self):
        critical = [v for v in self.violations if v["severity"] == "critical"]
        serious = [v for v in self.violations if v["severity"] == "serious"]
        moderate = [v for v in self.violations if v["severity"] == "moderate"]
        return {
            "level": self.level,
            "total_violations": len(self.violations),
            "critical": len(critical),
            "serious": len(serious),
            "moderate": len(moderate),
            "compliant": len(critical) == 0,
            "details": self.violations
        }

checker = WCAGComplianceChecker("AA")
report = checker.check_full_compliance("<html><body><img src='test.jpg'></body></html>")
print(f"合规: {report['compliant']}")
print(f"严重问题: {report['critical']}, 重要问题: {report['serious']}")
```

## 代码示例 (html)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Web Components 示例</title>
</head>
<body>
  <!-- 使用自定义组件 -->
  <product-card
    name="无线降噪耳机"
    price="1299"
    rating="4.5"
    image="headphones.jpg"
  ></product-card>

  <script>
    // 定义产品卡片组件
    class ProductCard extends HTMLElement {
      constructor() {
        super();
        // Shadow DOM 隔离样式
        const shadow = this.attachShadow({ mode: 'open' });

        shadow.innerHTML = `
          <style>
            :host {
              display: block;
              max-width: 300px;
              font-family: 'IBM Plex Sans', sans-serif;
            }
            .card {
              border: 1px solid #e0e0e0;
              border-radius: 12px;
              overflow: hidden;
              transition: transform 0.3s ease;
            }
            .card:hover { transform: translateY(-4px); }
            .card img { width: 100%; height: 200px; object-fit: cover; }
            .card-body { padding: 1rem; }
            .card-title { font-size: 1.1rem; font-weight: 600; margin: 0 0 0.5rem; }
            .card-price { color: #e94560; font-size: 1.3rem; font-weight: 700; }
            .card-rating { color: #f5a623; }
          </style>
          <div class="card">
            <img src="${this.getAttribute('image')}" alt="${this.getAttribute('name')}">
            <div class="card-body">
              <h3 class="card-title">${this.getAttribute('name')}</h3>
              <p class="card-price">¥${this.getAttribute('price')}</p>
              <p class="card-rating">评分: ${this.getAttribute('rating')}★</p>
            </div>
          </div>
        `;
      }

      // 生命周期: 挂载
      connectedCallback() {
        console.log('产品卡片已挂载');
      }

      // 生命周期: 卸载
      disconnectedCallback() {
        console.log('产品卡片已卸载');
      }

      // 属性变化监听
      static get observedAttributes() {
        return ['name', 'price', 'rating', 'image'];
      }

      attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
          console.log(`属性 ${name} 变更: ${oldValue} → ${newValue}`);
        }
      }
    }

    // 注册自定义元素
    customElements.define('product-card', ProductCard);
  </script>
</body>
</html>
```

