"""
Invoice Forge - Template Engine
Generate professional HTML invoices with print-ready CSS.

Author: Shadow Rose
License: MIT
"""

from typing import Dict, List
from datetime import datetime
import base64
import os


class InvoiceTemplate:
    """Generate professional invoice HTML."""
    
    @staticmethod
    def format_currency(amount: float, symbol: str = "$", code: str = "USD") -> str:
        """Format amount as currency."""
        return f"{symbol}{amount:,.2f}"
    
    @staticmethod
    def _embed_logo(logo_path: str) -> str:
        """Embed logo as base64 data URL."""
        if not logo_path or not os.path.exists(logo_path):
            return ""
        
        try:
            with open(logo_path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            
            ext = logo_path.lower().split(".")[-1]
            mime_types = {
                "png": "image/png",
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "gif": "image/gif",
                "svg": "image/svg+xml",
            }
            mime = mime_types.get(ext, "image/png")
            
            return f'<img src="data:{mime};base64,{data}" alt="Logo" class="logo">'
        except Exception:
            return ""
    
    @staticmethod
    def render_html(invoice_data: Dict, config: Dict) -> str:
        """
        Render invoice as professional HTML.
        
        Args:
            invoice_data: Invoice data dictionary
            config: Configuration dictionary with business details
        
        Returns:
            HTML string
        """
        # Extract data
        invoice_number = invoice_data.get("invoice_number", "")
        invoice_date = invoice_data.get("invoice_date", "")
        due_date = invoice_data.get("due_date", "")
        
        business = {
            "name": config.get("BUSINESS_NAME", ""),
            "address": config.get("BUSINESS_ADDRESS", ""),
            "email": config.get("BUSINESS_EMAIL", ""),
            "phone": config.get("BUSINESS_PHONE", ""),
            "website": config.get("BUSINESS_WEBSITE", ""),
            "logo": config.get("BUSINESS_LOGO", None),
        }
        
        client = invoice_data.get("client", {})
        items = invoice_data.get("items", [])
        
        subtotal = invoice_data.get("subtotal", 0.0)
        discount_amount = invoice_data.get("discount_amount", 0.0)
        tax_amount = invoice_data.get("tax_amount", 0.0)
        total = invoice_data.get("total", 0.0)
        
        tax_label = invoice_data.get("tax_label", "Tax")
        discount_info = invoice_data.get("discount_info", "")
        
        currency_symbol = config.get("CURRENCY_SYMBOL", "$")
        payment_details = config.get("PAYMENT_DETAILS", "")
        notes = invoice_data.get("notes", "")
        terms = invoice_data.get("terms", "")
        
        # Format currency helper
        def fmt(amount):
            return InvoiceTemplate.format_currency(amount, currency_symbol)
        
        # Build logo HTML
        logo_html = ""
        if business["logo"]:
            logo_html = InvoiceTemplate._embed_logo(business["logo"])
        
        # Build items HTML
        items_html = ""
        for item in items:
            desc = item.get("description", "")
            qty = item.get("quantity", 0)
            rate = item.get("rate", 0.0)
            amount = item.get("amount", 0.0)
            
            items_html += f"""
            <tr>
                <td>{desc}</td>
                <td class="text-right">{qty}</td>
                <td class="text-right">{fmt(rate)}</td>
                <td class="text-right amount">{fmt(amount)}</td>
            </tr>
            """
        
        # Build discount row
        discount_html = ""
        if discount_amount > 0:
            discount_html = f"""
            <tr>
                <td colspan="3" class="text-right">Discount {discount_info}</td>
                <td class="text-right amount">-{fmt(discount_amount)}</td>
            </tr>
            """
        
        # Build tax row
        tax_html = ""
        if tax_amount > 0:
            tax_html = f"""
            <tr>
                <td colspan="3" class="text-right">{tax_label}</td>
                <td class="text-right amount">{fmt(tax_amount)}</td>
            </tr>
            """
        
        # Payment status badge
        status = invoice_data.get("status", "pending")
        status_class = {
            "paid": "status-paid",
            "pending": "status-pending",
            "overdue": "status-overdue",
            "cancelled": "status-cancelled",
        }.get(status, "status-pending")
        
        status_text = status.upper()
        
        # Full HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice {invoice_number}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .invoice {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 40px;
            border-bottom: 3px solid #333;
            padding-bottom: 20px;
        }}
        
        .logo {{
            max-width: 200px;
            max-height: 80px;
        }}
        
        .business-info {{
            flex: 1;
        }}
        
        .business-info h1 {{
            font-size: 24px;
            margin-bottom: 10px;
            color: #000;
        }}
        
        .business-info p {{
            font-size: 13px;
            color: #666;
            margin: 2px 0;
        }}
        
        .invoice-info {{
            text-align: right;
        }}
        
        .invoice-info h2 {{
            font-size: 28px;
            margin-bottom: 10px;
            color: #000;
        }}
        
        .invoice-info p {{
            font-size: 13px;
            margin: 5px 0;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            margin-top: 10px;
        }}
        
        .status-paid {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-pending {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .status-overdue {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .status-cancelled {{
            background: #e2e3e5;
            color: #383d41;
        }}
        
        .parties {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
        }}
        
        .party {{
            flex: 1;
        }}
        
        .party h3 {{
            font-size: 14px;
            text-transform: uppercase;
            color: #999;
            margin-bottom: 10px;
        }}
        
        .party p {{
            font-size: 14px;
            margin: 3px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
        }}
        
        thead {{
            background: #f8f9fa;
        }}
        
        th {{
            text-align: left;
            padding: 12px;
            font-size: 12px;
            text-transform: uppercase;
            color: #666;
            border-bottom: 2px solid #dee2e6;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
            font-size: 14px;
        }}
        
        .text-right {{
            text-align: right;
        }}
        
        .amount {{
            font-weight: 600;
        }}
        
        .totals {{
            margin-left: auto;
            width: 300px;
        }}
        
        .totals table {{
            margin: 0;
        }}
        
        .totals td {{
            border: none;
            padding: 8px 12px;
        }}
        
        .totals .total-row {{
            background: #f8f9fa;
            font-size: 18px;
            font-weight: bold;
        }}
        
        .payment-details {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-left: 4px solid #333;
        }}
        
        .payment-details h3 {{
            font-size: 14px;
            text-transform: uppercase;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .payment-details pre {{
            font-family: inherit;
            white-space: pre-wrap;
            font-size: 13px;
            line-height: 1.8;
        }}
        
        .notes {{
            margin: 20px 0;
            font-size: 13px;
            color: #666;
        }}
        
        .terms {{
            margin: 20px 0;
            padding: 15px;
            background: #fffbf0;
            border: 1px solid #ffe69c;
            font-size: 12px;
            color: #856404;
        }}
        
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            text-align: center;
            font-size: 12px;
            color: #999;
        }}
        
        /* Print styles */
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .invoice {{
                box-shadow: none;
                padding: 20px;
            }}
            
            .status-badge {{
                border: 1px solid currentColor;
            }}
        }}
    </style>
</head>
<body>
    <div class="invoice">
        <div class="header">
            <div class="business-info">
                {logo_html}
                <h1>{business['name']}</h1>
                <p>{business['address'].replace(chr(10), '<br>')}</p>
                <p>{business['email']}</p>
                <p>{business['phone']}</p>
                {f"<p>{business['website']}</p>" if business['website'] else ""}
            </div>
            <div class="invoice-info">
                <h2>INVOICE</h2>
                <p><strong>Invoice #:</strong> {invoice_number}</p>
                <p><strong>Date:</strong> {invoice_date}</p>
                <p><strong>Due Date:</strong> {due_date}</p>
                <span class="status-badge {status_class}">{status_text}</span>
            </div>
        </div>
        
        <div class="parties">
            <div class="party">
                <h3>Bill To</h3>
                <p><strong>{client.get('name', '')}</strong></p>
                <p>{client.get('email', '')}</p>
                {f"<p>{client.get('address', '').replace(chr(10), '<br>')}</p>" if client.get('address') else ""}
                {f"<p>{client.get('phone', '')}</p>" if client.get('phone') else ""}
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Description</th>
                    <th class="text-right">Quantity</th>
                    <th class="text-right">Rate</th>
                    <th class="text-right">Amount</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>
        
        <div class="totals">
            <table>
                <tr>
                    <td class="text-right">Subtotal</td>
                    <td class="text-right amount">{fmt(subtotal)}</td>
                </tr>
                {discount_html}
                {tax_html}
                <tr class="total-row">
                    <td class="text-right">TOTAL</td>
                    <td class="text-right">{fmt(total)}</td>
                </tr>
            </table>
        </div>
        
        {f'''<div class="payment-details">
            <h3>Payment Details</h3>
            <pre>{payment_details}</pre>
        </div>''' if payment_details else ''}
        
        {f'<div class="notes"><strong>Notes:</strong> {notes}</div>' if notes else ''}
        
        {f'<div class="terms"><strong>Terms:</strong> {terms}</div>' if terms else ''}
        
        <div class="footer">
            <p>Generated by Invoice Forge • {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    @staticmethod
    def render_markdown(invoice_data: Dict, config: Dict) -> str:
        """
        Render invoice as Markdown.
        
        Args:
            invoice_data: Invoice data dictionary
            config: Configuration dictionary
        
        Returns:
            Markdown string
        """
        invoice_number = invoice_data.get("invoice_number", "")
        invoice_date = invoice_data.get("invoice_date", "")
        due_date = invoice_data.get("due_date", "")
        status = invoice_data.get("status", "pending").upper()
        
        business_name = config.get("BUSINESS_NAME", "")
        business_address = config.get("BUSINESS_ADDRESS", "")
        business_email = config.get("BUSINESS_EMAIL", "")
        business_phone = config.get("BUSINESS_PHONE", "")
        
        client = invoice_data.get("client", {})
        items = invoice_data.get("items", [])
        
        subtotal = invoice_data.get("subtotal", 0.0)
        discount_amount = invoice_data.get("discount_amount", 0.0)
        tax_amount = invoice_data.get("tax_amount", 0.0)
        total = invoice_data.get("total", 0.0)
        
        tax_label = invoice_data.get("tax_label", "Tax")
        discount_info = invoice_data.get("discount_info", "")
        
        currency_symbol = config.get("CURRENCY_SYMBOL", "$")
        payment_details = config.get("PAYMENT_DETAILS", "")
        notes = invoice_data.get("notes", "")
        terms = invoice_data.get("terms", "")
        
        def fmt(amount):
            return f"{currency_symbol}{amount:,.2f}"
        
        # Build markdown
        md = f"""# INVOICE {invoice_number}

**Status:** {status}

---

## {business_name}

{business_address}  
{business_email}  
{business_phone}

**Invoice Date:** {invoice_date}  
**Due Date:** {due_date}

---

## Bill To

**{client.get('name', '')}**  
{client.get('email', '')}  
{client.get('address', '').replace(chr(10), '  ' + chr(10))}  
{client.get('phone', '')}

---

## Invoice Items

| Description | Quantity | Rate | Amount |
|------------|----------|------|--------|
"""
        
        for item in items:
            desc = item.get("description", "")
            qty = item.get("quantity", 0)
            rate = item.get("rate", 0.0)
            amount = item.get("amount", 0.0)
            md += f"| {desc} | {qty} | {fmt(rate)} | {fmt(amount)} |\n"
        
        md += f"""
---

## Summary

**Subtotal:** {fmt(subtotal)}
"""
        
        if discount_amount > 0:
            md += f"**Discount {discount_info}:** -{fmt(discount_amount)}\n"
        
        if tax_amount > 0:
            md += f"**{tax_label}:** {fmt(tax_amount)}\n"
        
        md += f"""
**TOTAL:** {fmt(total)}

---

"""
        
        if payment_details:
            md += f"""## Payment Details

{payment_details}

---

"""
        
        if notes:
            md += f"""## Notes

{notes}

"""
        
        if terms:
            md += f"""## Terms

{terms}

"""
        
        md += f"\n*Generated by Invoice Forge • {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
        
        return md
    
    @staticmethod
    def render_text(invoice_data: Dict, config: Dict) -> str:
        """
        Render invoice as plain text.
        
        Args:
            invoice_data: Invoice data dictionary
            config: Configuration dictionary
        
        Returns:
            Plain text string
        """
        invoice_number = invoice_data.get("invoice_number", "")
        invoice_date = invoice_data.get("invoice_date", "")
        due_date = invoice_data.get("due_date", "")
        status = invoice_data.get("status", "pending").upper()
        
        business_name = config.get("BUSINESS_NAME", "")
        business_address = config.get("BUSINESS_ADDRESS", "")
        business_email = config.get("BUSINESS_EMAIL", "")
        business_phone = config.get("BUSINESS_PHONE", "")
        
        client = invoice_data.get("client", {})
        items = invoice_data.get("items", [])
        
        subtotal = invoice_data.get("subtotal", 0.0)
        discount_amount = invoice_data.get("discount_amount", 0.0)
        tax_amount = invoice_data.get("tax_amount", 0.0)
        total = invoice_data.get("total", 0.0)
        
        tax_label = invoice_data.get("tax_label", "Tax")
        discount_info = invoice_data.get("discount_info", "")
        
        currency_symbol = config.get("CURRENCY_SYMBOL", "$")
        payment_details = config.get("PAYMENT_DETAILS", "")
        notes = invoice_data.get("notes", "")
        terms = invoice_data.get("terms", "")
        
        def fmt(amount):
            return f"{currency_symbol}{amount:,.2f}"
        
        # Build plain text
        text = f"""
{'=' * 80}
INVOICE {invoice_number}
Status: {status}
{'=' * 80}

{business_name}
{business_address}
{business_email}
{business_phone}

Invoice Date: {invoice_date}
Due Date:     {due_date}

{'=' * 80}
BILL TO
{'=' * 80}

{client.get('name', '')}
{client.get('email', '')}
{client.get('address', '')}
{client.get('phone', '')}

{'=' * 80}
ITEMS
{'=' * 80}

{'Description':<40} {'Qty':>8} {'Rate':>12} {'Amount':>12}
{'-' * 80}
"""
        
        for item in items:
            desc = item.get("description", "")[:40]
            qty = item.get("quantity", 0)
            rate = item.get("rate", 0.0)
            amount = item.get("amount", 0.0)
            text += f"{desc:<40} {qty:>8} {fmt(rate):>12} {fmt(amount):>12}\n"
        
        text += f"""
{'-' * 80}

{'Subtotal':>68} {fmt(subtotal):>12}
"""
        
        if discount_amount > 0:
            text += f"{'Discount ' + discount_info:>68} {'-' + fmt(discount_amount):>12}\n"
        
        if tax_amount > 0:
            text += f"{tax_label:>68} {fmt(tax_amount):>12}\n"
        
        text += f"""
{'TOTAL':>68} {fmt(total):>12}

{'=' * 80}
"""
        
        if payment_details:
            text += f"""
PAYMENT DETAILS
{'=' * 80}

{payment_details}

"""
        
        if notes:
            text += f"""
NOTES
{'=' * 80}

{notes}

"""
        
        if terms:
            text += f"""
TERMS
{'=' * 80}

{terms}

"""
        
        text += f"\nGenerated by Invoice Forge • {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        
        return text
