#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发票附件识别的回归测试（纯标准库，直接 python3 运行）。

覆盖历史事故：邮件正文 HTML 以 '<' 开头，被魔数嗅探判成 XML 发票，
导致六要素全空 → 抬头比对失败 → 全部记成「跳过」（静默漏发）。
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import invoice_forward as F  # noqa: E402
from email import message_from_bytes  # noqa: E402

HTML_BODY = ("<!DOCTYPE html><html><head><meta charset='utf-8'></head>"
             "<body><p>尊敬的客户，您有一张电子发票</p></body></html>")
PDF_BYTES = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF\n"
OFD_BYTES = b"PK\x03\x04" + b"\x00" * 60
XML_BYTES = ('<?xml version="1.0" encoding="utf-8"?>'
             '<EInvoice><InvoiceNumber>12345678901234567890</InvoiceNumber></EInvoice>'
             ).encode("utf-8")


def build(raw):
    return message_from_bytes(raw.encode("utf-8") if isinstance(raw, str) else raw)


class AttachmentDetectTest(unittest.TestCase):
    def test_html_body_is_not_an_invoice(self):
        """纯正文 HTML（无附件）不得被识别为 XML 发票。"""
        msg = build(
            "MIME-Version: 1.0\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n" + HTML_BODY)
        self.assertEqual(F.detect_fmt_from_magic(HTML_BODY.encode("utf-8")), "")
        self.assertEqual(F.find_invoice_attachment(msg), (b"", "", ""))

    def test_html_body_plus_pdf_picks_pdf(self):
        """正文 HTML 在前、PDF 附件在后：必须拿到 PDF，不能拿正文。"""
        msg = build(
            "MIME-Version: 1.0\r\n"
            "Content-Type: multipart/mixed; boundary=B\r\n"
            "\r\n--B\r\n"
            "Content-Type: text/html; charset=utf-8\r\n\r\n" + HTML_BODY + "\r\n"
            "--B\r\n"
            "Content-Type: application/octet-stream\r\n"
            "Content-Disposition: attachment; filename=\"26337000000882458978.pdf\"\r\n"
            "Content-Transfer-Encoding: base64\r\n\r\n"
            "JVBERi0xLjQKJeLjz9MKMQowIG9iago8PD4+CmVuZG9iagp0cmFpbGVyCjw8Pj4KJSVFT0YK\r\n"
            "--B--\r\n")
        data, fname, fmt = F.find_invoice_attachment(msg)
        self.assertEqual(fmt, "pdf")
        self.assertEqual(fname, "26337000000882458978.pdf")
        self.assertTrue(data.startswith(b"%PDF"))

    def test_pdf_wins_over_xml_when_both_present(self):
        """同时有 PDF / OFD / XML 时取 PDF（转发只带 PDF）。"""
        msg = build(
            "MIME-Version: 1.0\r\n"
            "Content-Type: multipart/mixed; boundary=B\r\n"
            "\r\n--B\r\n"
            "Content-Type: application/octet-stream\r\n"
            "Content-Disposition: attachment; filename=\"a.xml\"\r\n\r\n"
            '<?xml version="1.0"?><EInvoice><X>1</X></EInvoice>\r\n'
            "--B\r\n"
            "Content-Type: application/octet-stream\r\n"
            "Content-Disposition: attachment; filename=\"a.pdf\"\r\n"
            "Content-Transfer-Encoding: base64\r\n\r\n"
            "JVBERi0xLjQKJeLjz9MKMQowIG9iago8PD4+CmVuZG9iagp0cmFpbGVyCjw8Pj4KJSVFT0YK\r\n"
            "--B--\r\n")
        _, fname, fmt = F.find_invoice_attachment(msg)
        self.assertEqual(fmt, "pdf")
        self.assertEqual(fname, "a.pdf")

    def test_folded_rfc2047_chinese_filename(self):
        """票通类：附件名是 Q 编码 + 折行，必须解码后仍识别为 PDF。"""
        msg = build(
            "MIME-Version: 1.0\r\n"
            "Content-Type: multipart/mixed; boundary=B\r\n"
            "\r\n--B\r\n"
            "Content-Type: text/html; charset=utf-8\r\n\r\n" + HTML_BODY + "\r\n"
            "--B\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "Content-Disposition: attachment;\r\n"
            "\tfilename=\"=?UTF-8?Q?263120000065599648?=\r\n"
            " =?UTF-8?Q?81=5F=E4=B8=8A=E6=B5=B7.pdf?=\"\r\n"
            "Content-Transfer-Encoding: base64\r\n\r\n"
            "JVBERi0xLjQKJeLjz9MKMQowIG9iago8PD4+CmVuZG9iagp0cmFpbGVyCjw8Pj4KJSVFT0YK\r\n"
            "--B--\r\n")
        data, fname, fmt = F.find_invoice_attachment(msg)
        self.assertEqual(fmt, "pdf")
        self.assertIn("263120000065599648", fname)
        self.assertIn("上海", fname)

    def test_real_invoice_xml_still_detected(self):
        """真发票 XML 不能被误杀。"""
        self.assertEqual(F.detect_fmt_from_magic(XML_BYTES), "xml")

    def test_xml_named_but_html_content_is_rejected(self):
        """名为 .xml、实为正文 HTML 的附件要丢弃，回落到真正的 PDF。"""
        msg = build(
            "MIME-Version: 1.0\r\n"
            "Content-Type: multipart/mixed; boundary=B\r\n"
            "\r\n--B\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Disposition: attachment; filename=\"invoice.xml\"\r\n\r\n"
            + HTML_BODY + "\r\n"
            "--B\r\n"
            "Content-Type: application/pdf\r\n"
            "Content-Disposition: attachment; filename=\"invoice.pdf\"\r\n"
            "Content-Transfer-Encoding: base64\r\n\r\n"
            "JVBERi0xLjQKJeLjz9MKMQowIG9iago8PD4+CmVuZG9iagp0cmFpbGVyCjw8Pj4KJSVFT0YK\r\n"
            "--B--\r\n")
        _, fname, fmt = F.find_invoice_attachment(msg)
        self.assertEqual(fmt, "pdf")
        self.assertEqual(fname, "invoice.pdf")


class ExtractTest(unittest.TestCase):
    # 数电票版式：购销双方同处一行，label 与值被列排版拆开
    SAMPLE = ("电子发票（普通发票）\n发票号码：26337000000882458978\n开票日期：2026年10月17日\n"
              "购 销\n买 名称:上海研盛生物科技有限公司 售 名称:沃尔玛（浙江）百货有限公司杭州西溪山姆会员商店\n"
              "方 方\n*水果*福安巨峰葡萄1.4KG. 1.4kg. 盒 1 36.61 36.61 9% 3.29\n"
              "价税合计（大写） 贰佰伍拾玖圆叁角整 （小写）¥259.30\n")

    def test_buyer_is_first_name(self):
        f = F.extract(self.SAMPLE)
        self.assertEqual(f["buyer"], "上海研盛生物科技有限公司")

    def test_seller_falls_back_to_second_name(self):
        f = F.extract(self.SAMPLE)
        self.assertEqual(f["seller"], "沃尔玛（浙江）百货有限公司杭州西溪山姆会员商店")

    def test_amount_and_no(self):
        f = F.extract(self.SAMPLE)
        self.assertEqual(f["amount"], "259.30")
        self.assertEqual(f["invoice_no"], "26337000000882458978")
        self.assertEqual(f["date"], "2026年10月17日")


if __name__ == "__main__":
    unittest.main(verbosity=2)
