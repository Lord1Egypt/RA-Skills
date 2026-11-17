# kechuang-collection

从固定的政府网站白名单检索科创公告，按 KPI 分类并输出可人工复核的线索摘要。

## 使用

将此目录作为技能安装后，可使用：

```text
/kechuang-collection scan 高新技术企业 认定 --days=30
/kechuang-collection report
/kechuang-collection list-sources
/kechuang-collection scan 科技奖 --mock
```

此版本不接受自定义来源，不启动后台循环，也不默认写入本地文件。联网模式会把检索词发送给搜索服务；不要把未公开项目名、个人信息或秘密放入查询。

## License

MIT
