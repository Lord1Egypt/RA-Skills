#!/usr/bin/env python3
"""
pm-proto-prd-pin 2.1.0 植入脚本。

用法：
  python3 inject.py <目标原型目录>

行为：
  1. 复制 prd-pin-tool.js、prd-groups.js、prd-hook-templates.js 与 vendor 到目标目录 assets/。
  2. 复制 server.js 与 start.sh（本地持久化模式需要）。
  3. 为每个 .html 生成双常量数据文件 prd-data-<name>.js。
  4. 在 </body> 前注入配置块与三个脚本引用。

安全：
  skill 与注入产物都不写任何密钥、Token 或项目地址。
  网关地址由目标项目注入 window.PRD_CLOUDFLARE_URL。
  管理员密钥只存环境变量或本地密码管理器。
"""

import os
import sys
import shutil

CACHE_VERSION = '2.1.0'

CONFIG_TEMPLATE = '''  <!-- PRD 打点工具配置。禁止在此写入任何密钥、Token 或凭据。 -->
  <script>
  (function () {
    /* 目标项目网关地址。留空时由工具配置面板填写；不含密钥。 */
    window.PRD_CLOUDFLARE_URL = '';
    window.PRD_PAGE_FILES = [
__PAGE_FILES__
    ];
    /* 初始分组、视图中文名与跳转函数。按目标项目补充。 */
    window.PRD_GROUP_PRESET = [];
    window.PRD_VIEW_LABELS = {};
    window.PRD_VIEW_JUMPS = {};
    /* 定位钩子配置。实现位于 prd-hook-templates.js，与当前工具行为一致。
       按目标项目补齐 containerHints、titleViewHints、modalOpeners、prepareAnchor、switchView。
       prepareAnchor 只在锚点藏在向导步骤或分步表单里时使用，必须幂等。 */
    window.PRD_HOOK_CONFIG = {
      containerHints: [],
      titleViewHints: {},
      dynamicPattern: /(?:)/,
      modalOpeners: [],
      prepareAnchor: null,
      switchView: function (viewKey) {
        if (window.UI && typeof UI.showView === 'function') UI.showView(viewKey);
      },
      currentView: function () { return ''; },
      scope: function () { return { top: '', home: '' }; }
    };
  })();
  </script>
'''

DATA_TEMPLATE = '''/**
 * __HTML_FILE__ 专属 PRD 规格数据。
 * 作用: file:// 直开时的本地兜底；http/线上环境下由云端数据热替换。
 * PAGE_PRD_DATA 与 PRD_VERSION_REGISTRY 双常量同源。
 */
window.PAGE_PRD_DATA = window.PAGE_PRD_DATA || {};
window.PAGE_PRD_DATA["__HTML_FILE__"] = [];
window.INITIAL_PRD_DATA = window.PAGE_PRD_DATA["__HTML_FILE__"];
window.PRD_VERSION_REGISTRY = {
  "activeVersion": "v1.0.0",
  "versions": {
    "v1.0.0": []
  }
};
'''


def build_config_block(page_files):
    files = ',\n'.join(
        '      { label: "' + os.path.splitext(f)[0] + '", url: "./' + f + '" }'
        for f in page_files
    )
    return CONFIG_TEMPLATE.replace('__PAGE_FILES__', files)


def build_data_file(html_file):
    return DATA_TEMPLATE.replace('__HTML_FILE__', html_file)


def main():
    if len(sys.argv) < 2:
        print('用法: python3 inject.py <目标原型目录>')
        sys.exit(1)

    target = os.path.abspath(sys.argv[1])
    if not os.path.isdir(target):
        print('错误: 目标目录不存在: ' + target)
        sys.exit(1)

    skill_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    assets = os.path.join(skill_root, 'assets')
    target_js = os.path.join(target, 'assets', 'js')
    os.makedirs(target_js, exist_ok=True)

    for name in ('prd-pin-tool.js', 'prd-groups.js', 'prd-hook-templates.js'):
        src = os.path.join(assets, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(target_js, name))
            print('已植入: assets/js/' + name)

    vendor_src = os.path.join(assets, 'vendor')
    vendor_dst = os.path.join(target, 'assets', 'vendor')
    if os.path.isdir(vendor_src):
        if os.path.isdir(vendor_dst):
            shutil.rmtree(vendor_dst)
        shutil.copytree(vendor_src, vendor_dst)
        print('已植入: assets/vendor/')

    for name in ('server.js', 'start.sh'):
        src = os.path.join(assets, name)
        dst = os.path.join(target, name)
        if os.path.isfile(src) and not os.path.isfile(dst):
            shutil.copy2(src, dst)
            if name.endswith('.sh'):
                os.chmod(dst, 0o755)
            print('已植入: ' + name)

    html_files = sorted(f for f in os.listdir(target) if f.lower().endswith('.html'))
    if not html_files:
        print('未发现 .html 文件')
        return

    config = build_config_block(html_files)

    for html_file in html_files:
        data_name = 'prd-data-' + os.path.splitext(html_file)[0] + '.js'
        data_path = os.path.join(target_js, data_name)
        if not os.path.isfile(data_path):
            with open(data_path, 'w', encoding='utf-8') as fh:
                fh.write(build_data_file(html_file))
            print('已初始化: assets/js/' + data_name)

        html_path = os.path.join(target, html_file)
        with open(html_path, 'r', encoding='utf-8') as fh:
            content = fh.read()

        if 'prd-pin-tool.js' not in content:
            scripts = (
                '\n  <!-- 交互式 PRD 打点与规约标注引擎 -->\n'
                + config
                + '  <script src="assets/js/' + data_name + '"></script>\n'
                + '  <script src="assets/js/prd-hook-templates.js?v=' + CACHE_VERSION + '"></script>\n'
                + '  <script src="assets/js/prd-pin-tool.js?v=' + CACHE_VERSION + '"></script>\n'
            )
            if '</body>' in content:
                content = content.replace('</body>', scripts + '</body>')
            else:
                content += scripts
            with open(html_path, 'w', encoding='utf-8') as fh:
                fh.write(content)
            print('已注入: ' + html_file)
        else:
            print('已存在，跳过: ' + html_file)

    print('\n植入完成。密钥只存环境变量或本地密码管理器，禁止写入本节脚本或仓库。')


if __name__ == '__main__':
    main()
