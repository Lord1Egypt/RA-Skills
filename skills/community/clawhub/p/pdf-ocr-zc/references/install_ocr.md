# 安装 Tesseract 与 ocrmypdf（Windows）

## 1. 安装 Tesseract
1. 前往 https://github.com/UB-Mannheim/tesseract/wiki 下载对应 Windows 的 MSI 安装包（通常是 `tesseract‑5.3.1‑setup‑amd64.exe`）。
2. 双击运行安装程序，保持默认路径（如 `C:\Program Files\Tesseract-OCR`），并在安装选项中勾选 **Add to PATH**。
3. 安装完成后，打开 PowerShell，运行 `tesseract --version` 检查是否能正确输出版本信息。

## 2. 安装 ocrmypdf（Python 包）
```powershell
# 建议使用 Python 3.10+（已在工作区安装）
python -m pip install --upgrade pip
pip install ocrmypdf
```
ocrmypdf 会自动调用已在 PATH 中的 Tesseract。

## 3. 验证安装
```powershell
ocrmypdf --version
# 示例：对 test.pdf 生成带文字层的 PDF（仅作测试）
ocrmypdf test.pdf test_ocr.pdf
```
如果没有报错且生成了 `test_ocr.pdf`，说明已成功。

如需其他语言模型（如繁体中文、英文），可以在 Tesseract 安装目录的 `tessdata` 文件夹中放入对应的 `.traineddata` 文件，或使用 `pip install ocrmypdf[all]` 以获取额外依赖。
