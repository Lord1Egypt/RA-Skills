"""
Invoice Forge - Main Invoice Generator
Professional invoice generation for freelancers and small businesses.

Author: Shadow Rose
License: MIT
"""

import json
import os
import sys
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from invoice_clients import ClientManager
from invoice_template import InvoiceTemplate


class InvoiceForge:
    """Main invoice generation engine."""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize Invoice Forge.
        
        Args:
            config_file: Path to JSON config file (default: "config.json")
        """
        self.config = self._load_config(config_file)
        self.client_manager = ClientManager(self.config.get("CLIENTS_FILE", "data/clients.jsonl"))
        self.invoices_file = self.config.get("INVOICES_FILE", "data/invoices.jsonl")
        self.output_dir = self.config.get("OUTPUT_DIR", "output")
        self._ensure_dirs()
        self._load_invoice_counter()
    
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file."""
        for path in (config_file, "config_example.json"):
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Warning: Could not parse {path}: {e}")
        print("Warning: No config file found. Using built-in defaults.")
        return {}
    
    def _ensure_dirs(self):
        """Create necessary directories."""
        if self.config.get("AUTO_CREATE_DIRS", True):
            for directory in [
                os.path.dirname(self.invoices_file),
                os.path.dirname(self.config.get("CLIENTS_FILE", "data/clients.jsonl")),
                self.output_dir,
                self.config.get("TEMPLATES_DIR", "data/templates"),
            ]:
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
    
    def _load_invoice_counter(self):
        """Load the next invoice number from history."""
        self.invoice_counter = self.config.get("INVOICE_START", 1)
        
        if os.path.exists(self.invoices_file):
            with open(self.invoices_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        invoice = json.loads(line)
                        # Extract number from invoice_number
                        inv_num_str = invoice.get("invoice_number", "")
                        prefix = self.config.get("INVOICE_PREFIX", "INV-")
                        if inv_num_str.startswith(prefix):
                            try:
                                num = int(inv_num_str[len(prefix):])
                                self.invoice_counter = max(self.invoice_counter, num + 1)
                            except ValueError:
                                pass
    
    def _generate_invoice_number(self) -> str:
        """Generate next invoice number."""
        prefix = self.config.get("INVOICE_PREFIX", "INV-")
        padding = self.config.get("INVOICE_PADDING", 4)
        number = str(self.invoice_counter).zfill(padding)
        self.invoice_counter += 1
        return f"{prefix}{number}"
    
    def _calculate_totals(self, items: List[Dict], discount: Dict, tax_rate: float) -> Tuple[float, float, float, float]:
        """
        Calculate invoice totals.
        
        Args:
            items: List of line items
            discount: Discount dict {"type": "percent"|"flat", "value": float}
            tax_rate: Tax rate as decimal (e.g., 0.08 for 8%)
        
        Returns:
            (subtotal, discount_amount, tax_amount, total)
        """
        # Calculate subtotal
        subtotal = sum(item.get("amount", 0.0) for item in items)
        
        # Calculate discount
        discount_amount = 0.0
        if discount:
            if discount.get("type") == "percent":
                discount_amount = subtotal * (discount.get("value", 0.0) / 100.0)
            elif discount.get("type") == "flat":
                discount_amount = discount.get("value", 0.0)
        
        # Calculate tax on discounted amount
        taxable = subtotal - discount_amount
        tax_amount = taxable * tax_rate
        
        # Calculate total
        total = taxable + tax_amount
        
        return (subtotal, discount_amount, tax_amount, total)
    
    def create_invoice(
        self,
        client_id: str,
        items: List[Dict],
        invoice_date: Optional[str] = None,
        payment_terms: Optional[int] = None,
        tax_type: Optional[str] = None,
        discount: Optional[Dict] = None,
        notes: str = "",
        status: str = "pending",
        invoice_number: Optional[str] = None,
    ) -> Dict:
        """
        Create a new invoice.
        
        Args:
            client_id: Client identifier
            items: List of line items [{"description": str, "quantity": int, "rate": float}]
            invoice_date: Invoice date (ISO format, default: today)
            payment_terms: Days until due (default: from config)
            tax_type: Tax type key (default: from config)
            discount: {"type": "percent"|"flat", "value": float}
            notes: Additional notes
            status: Invoice status (pending, paid, overdue, cancelled)
            invoice_number: Custom invoice number (default: auto-generated)
        
        Returns:
            Invoice data dictionary
        """
        # Get client
        client = self.client_manager.get_client(client_id)
        if not client:
            raise ValueError(f"Client not found: {client_id}")
        
        # Set defaults
        if invoice_date is None:
            invoice_date = datetime.now().strftime(self.config.get("DATE_FORMAT", "%Y-%m-%d"))
        
        if payment_terms is None:
            payment_terms = self.config.get("DEFAULT_PAYMENT_TERMS", 30)
        
        if tax_type is None:
            tax_type = self.config.get("DEFAULT_TAX_TYPE", "sales_tax")
        
        if discount is None:
            discount = {}
        
        # Calculate amounts for each item
        processed_items = []
        for item in items:
            qty = item.get("quantity", 1)
            rate = item.get("rate", 0.0)
            amount = qty * rate
            processed_items.append({
                "description": item.get("description", ""),
                "quantity": qty,
                "rate": rate,
                "amount": amount,
            })
        
        # Get tax rate
        tax_rates = self.config.get("TAX_RATES", {})
        tax_rate = tax_rates.get(tax_type, 0.0)
        tax_labels = self.config.get("TAX_LABELS", {})
        tax_label = tax_labels.get(tax_type, "Tax")
        
        # Calculate totals
        subtotal, discount_amount, tax_amount, total = self._calculate_totals(
            processed_items, discount, tax_rate
        )
        
        # Calculate due date
        invoice_dt = datetime.strptime(invoice_date, self.config.get("DATE_FORMAT", "%Y-%m-%d"))
        due_dt = invoice_dt + timedelta(days=payment_terms)
        due_date = due_dt.strftime(self.config.get("DATE_FORMAT", "%Y-%m-%d"))
        
        # Generate invoice number
        if invoice_number is None:
            invoice_number = self._generate_invoice_number()
        
        # Format discount info
        discount_info = ""
        if discount_amount > 0:
            if discount.get("type") == "percent":
                discount_info = f"({discount.get('value')}%)"
            else:
                discount_info = "(flat)"
        
        # Format terms text
        terms = self.config.get("DEFAULT_TERMS", "").format(days=payment_terms)
        
        # Build invoice data
        invoice_data = {
            "invoice_number": invoice_number,
            "invoice_date": invoice_date,
            "due_date": due_date,
            "client": {
                "client_id": client_id,
                "name": client.get("name", ""),
                "email": client.get("email", ""),
                "address": client.get("address", ""),
                "phone": client.get("phone", ""),
            },
            "items": processed_items,
            "subtotal": subtotal,
            "discount": discount,
            "discount_amount": discount_amount,
            "discount_info": discount_info,
            "tax_type": tax_type,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "tax_label": tax_label,
            "total": total,
            "currency_symbol": self.config.get("CURRENCY_SYMBOL", "$"),
            "currency_code": self.config.get("CURRENCY_CODE", "USD"),
            "notes": notes or self.config.get("DEFAULT_NOTES", ""),
            "terms": terms,
            "status": status,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        # Save to ledger
        self._save_invoice(invoice_data)
        
        return invoice_data
    
    def _save_invoice(self, invoice_data: Dict):
        """Save invoice to JSONL ledger."""
        with open(self.invoices_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(invoice_data) + "\n")
    
    def get_invoice(self, invoice_number: str) -> Optional[Dict]:
        """Get invoice by number."""
        if not os.path.exists(self.invoices_file):
            return None
        
        with open(self.invoices_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    invoice = json.loads(line)
                    if invoice.get("invoice_number") == invoice_number:
                        return invoice
        
        return None
    
    def list_invoices(self, client_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """
        List invoices, optionally filtered.
        
        Args:
            client_id: Filter by client
            status: Filter by status
        
        Returns:
            List of invoice dictionaries
        """
        if not os.path.exists(self.invoices_file):
            return []
        
        invoices = []
        with open(self.invoices_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    invoice = json.loads(line)
                    
                    # Apply filters
                    if client_id and invoice.get("client", {}).get("client_id") != client_id:
                        continue
                    
                    if status and invoice.get("status") != status:
                        continue
                    
                    invoices.append(invoice)
        
        # Sort by invoice date (newest first)
        invoices.sort(key=lambda inv: inv.get("invoice_date", ""), reverse=True)
        
        return invoices
    
    def update_invoice_status(self, invoice_number: str, status: str) -> bool:
        """Update invoice payment status."""
        invoices = self.list_invoices()
        updated = False
        
        for invoice in invoices:
            if invoice.get("invoice_number") == invoice_number:
                invoice["status"] = status
                invoice["updated_at"] = datetime.now().isoformat()
                updated = True
                break
        
        if not updated:
            return False
        
        # Rewrite file
        with open(self.invoices_file, "w", encoding="utf-8") as f:
            for invoice in invoices:
                f.write(json.dumps(invoice) + "\n")
        
        return True
    
    def render_invoice(self, invoice_data: Dict, format: str = "html") -> str:
        """
        Render invoice in specified format.
        
        Args:
            invoice_data: Invoice data dictionary
            format: Output format ("html", "markdown", "text")
        
        Returns:
            Rendered invoice string
        """
        if format == "html":
            return InvoiceTemplate.render_html(invoice_data, self.config)
        elif format == "markdown":
            return InvoiceTemplate.render_markdown(invoice_data, self.config)
        elif format == "text":
            return InvoiceTemplate.render_text(invoice_data, self.config)
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def save_rendered_invoice(self, invoice_data: Dict, format: str = "html") -> str:
        """
        Save rendered invoice to file.
        
        Args:
            invoice_data: Invoice data dictionary
            format: Output format
        
        Returns:
            Path to saved file
        """
        invoice_number = invoice_data.get("invoice_number", "invoice")
        
        extensions = {
            "html": ".html",
            "markdown": ".md",
            "text": ".txt",
        }
        
        ext = extensions.get(format, ".txt")
        filename = f"{invoice_number}{ext}"
        filepath = os.path.join(self.output_dir, filename)
        
        # Backup if exists
        if os.path.exists(filepath) and self.config.get("BACKUP_ON_OVERWRITE", True):
            backup = f"{filepath}.bak"
            if os.path.exists(backup):
                os.remove(backup)
            os.rename(filepath, backup)
        
        # Render and save
        content = self.render_invoice(invoice_data, format)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filepath
    
    def create_from_template(self, template_name: str, client_id: str, **overrides) -> Dict:
        """
        Create invoice from recurring template.
        
        Args:
            template_name: Template name from config
            client_id: Client identifier
            **overrides: Override template fields
        
        Returns:
            Invoice data dictionary
        """
        templates = self.config.get("RECURRING_TEMPLATES", {})
        template = templates.get(template_name)
        
        if not template:
            raise ValueError(f"Template not found: {template_name}")
        
        # Merge template with overrides
        params = {
            "client_id": client_id,
            "items": template.get("items", []),
            "payment_terms": template.get("payment_terms"),
            "notes": template.get("notes", ""),
        }
        params.update(overrides)
        
        return self.create_invoice(**params)


def main():
    """CLI for invoice generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Invoice Forge - Professional Invoice Generator")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create invoice
    create_parser = subparsers.add_parser("create", help="Create a new invoice")
    create_parser.add_argument("client_id", help="Client ID")
    create_parser.add_argument("--item", action="append", nargs=3, metavar=("DESC", "QTY", "RATE"),
                               help="Add line item (can be repeated)")
    create_parser.add_argument("--date", help="Invoice date (YYYY-MM-DD, default: today)")
    create_parser.add_argument("--terms", type=int, help="Payment terms in days")
    create_parser.add_argument("--tax", help="Tax type")
    create_parser.add_argument("--discount-percent", type=float, help="Discount percentage")
    create_parser.add_argument("--discount-flat", type=float, help="Flat discount amount")
    create_parser.add_argument("--notes", help="Additional notes")
    create_parser.add_argument("--status", default="pending", help="Invoice status")
    create_parser.add_argument("--format", default="html", choices=["html", "markdown", "text"],
                               help="Output format")
    create_parser.add_argument("--no-save", action="store_true", help="Don't save to file")
    
    # List invoices
    list_parser = subparsers.add_parser("list", help="List invoices")
    list_parser.add_argument("--client", help="Filter by client ID")
    list_parser.add_argument("--status", help="Filter by status")
    
    # Get invoice
    get_parser = subparsers.add_parser("get", help="Get invoice by number")
    get_parser.add_argument("invoice_number", help="Invoice number")
    get_parser.add_argument("--format", default="html", choices=["html", "markdown", "text"],
                            help="Output format")
    
    # Update status
    status_parser = subparsers.add_parser("status", help="Update invoice status")
    status_parser.add_argument("invoice_number", help="Invoice number")
    status_parser.add_argument("status", choices=["pending", "paid", "overdue", "cancelled"],
                               help="New status")
    
    # Create from template
    template_parser = subparsers.add_parser("template", help="Create from recurring template")
    template_parser.add_argument("template_name", help="Template name")
    template_parser.add_argument("client_id", help="Client ID")
    template_parser.add_argument("--format", default="html", choices=["html", "markdown", "text"],
                                 help="Output format")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    forge = InvoiceForge()
    
    if args.command == "create":
        if not args.item:
            print("Error: At least one --item is required")
            sys.exit(1)
        
        # Build items list
        items = []
        for desc, qty_str, rate_str in args.item:
            items.append({
                "description": desc,
                "quantity": int(qty_str),
                "rate": float(rate_str),
            })
        
        # Build discount
        discount = None
        if args.discount_percent:
            discount = {"type": "percent", "value": args.discount_percent}
        elif args.discount_flat:
            discount = {"type": "flat", "value": args.discount_flat}
        
        # Create invoice
        invoice = forge.create_invoice(
            client_id=args.client_id,
            items=items,
            invoice_date=args.date,
            payment_terms=args.terms,
            tax_type=args.tax,
            discount=discount,
            notes=args.notes or "",
            status=args.status,
        )
        
        print(f"✓ Invoice created: {invoice['invoice_number']}")
        print(f"  Total: {forge.config.get('CURRENCY_SYMBOL', '$')}{invoice['total']:,.2f}")
        
        if not args.no_save:
            filepath = forge.save_rendered_invoice(invoice, args.format)
            print(f"  Saved to: {filepath}")
    
    elif args.command == "list":
        invoices = forge.list_invoices(client_id=args.client, status=args.status)
        
        if not invoices:
            print("No invoices found.")
        else:
            print(f"{'Invoice #':<15} {'Date':<12} {'Client':<25} {'Total':>12} {'Status':<10}")
            print("-" * 80)
            for inv in invoices:
                inv_num = inv.get("invoice_number", "")
                inv_date = inv.get("invoice_date", "")
                client_name = inv.get("client", {}).get("name", "")[:25]
                total = inv.get("total", 0.0)
                status = inv.get("status", "")
                symbol = forge.config.get("CURRENCY_SYMBOL", "$")
                
                print(f"{inv_num:<15} {inv_date:<12} {client_name:<25} {symbol}{total:>11,.2f} {status:<10}")
    
    elif args.command == "get":
        invoice = forge.get_invoice(args.invoice_number)
        
        if not invoice:
            print(f"Invoice not found: {args.invoice_number}")
            sys.exit(1)
        
        rendered = forge.render_invoice(invoice, args.format)
        print(rendered)
    
    elif args.command == "status":
        if forge.update_invoice_status(args.invoice_number, args.status):
            print(f"✓ Invoice {args.invoice_number} status updated to: {args.status}")
        else:
            print(f"Invoice not found: {args.invoice_number}")
            sys.exit(1)
    
    elif args.command == "template":
        invoice = forge.create_from_template(args.template_name, args.client_id)
        
        print(f"✓ Invoice created from template: {invoice['invoice_number']}")
        print(f"  Total: {forge.config.get('CURRENCY_SYMBOL', '$')}{invoice['total']:,.2f}")
        
        filepath = forge.save_rendered_invoice(invoice, args.format)
        print(f"  Saved to: {filepath}")


if __name__ == "__main__":
    main()
