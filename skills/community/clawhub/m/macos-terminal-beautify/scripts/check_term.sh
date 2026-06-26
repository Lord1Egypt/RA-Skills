#!/bin/bash
echo "===== 1. Nerd Font 已安装 ====="
fc-list | grep -i "nerd font" | awk -F: '{print "  -", $2}' | sort -u | head

echo ""
echo "===== 2. 图标渲染测试 (看到符号 = OK, 方框 = 字体问题) ====="
printf "  FontAwesome apple (U+F179):  \uF179\n"
printf "  MDI apple (U+F0035):         \U000F0035\n"
printf "  Git branch (U+E0A0):         \uE0A0\n"
printf "  Folder (U+F07B):             \uF07B\n"
printf "  Powerline arrow (U+E0B0):    \uE0B0\n"

echo ""
echo "===== 3. 工具版本 ====="
echo "  Starship: $(starship --version 2>/dev/null || echo '未安装')"
echo "  Zsh: $(zsh --version 2>/dev/null || echo '未安装')"
echo "  Ghostty: $(ghostty --version 2>/dev/null || echo '未安装(但已安装到 Applications)')"
echo "  Oh My Zsh: $(ls -d ~/.oh-my-zsh 2>/dev/null && echo '已安装' || echo '未安装')"

echo ""
echo "===== 4. 配置文件存在性 ====="
for f in ~/.zshrc ~/.config/starship.toml ~/.config/ghostty/config; do
  [ -f "$f" ] && echo "  ✓ $f" || echo "  ✗ $f (缺失)"
done

echo ""
echo "===== 5. 插件安装状态 ====="
for p in zsh-autosuggestions zsh-syntax-highlighting zsh-completions; do
  [ -d ~/.oh-my-zsh/custom/plugins/$p ] && echo "  ✓ $p" || echo "  ✗ $p (缺失)"
done

echo ""
echo "===== 6. 环境变量 ====="
echo "  TERM=$TERM"
echo "  LANG=$LANG"
echo ""
echo "===== 自检完成 ====="
