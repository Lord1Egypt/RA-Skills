#!/bin/bash
# Basic functionality test for Invoice Forge
# Run this after setup to verify everything works

set -e

echo "=== Invoice Forge Basic Test ==="
echo ""

echo "1. Testing client management..."
python3 invoice_clients.py add demo_client "Demo Corp" "demo@example.com" "456 Demo St" "+1-555-9999"
python3 invoice_clients.py list

echo ""
echo "2. Creating test invoice..."
python3 invoice_forge.py create demo_client \
  --item "Consulting Services" 10 150.00 \
  --item "Travel Expenses" 1 250.00 \
  --terms 30

echo ""
echo "3. Listing invoices..."
python3 invoice_forge.py list

echo ""
echo "4. Testing reports..."
python3 invoice_report.py summary

echo ""
echo "5. Testing status update..."
python3 invoice_forge.py status INV-0001 paid
python3 invoice_forge.py list

echo ""
echo "6. Testing discount..."
python3 invoice_forge.py create demo_client \
  --item "Web Development" 40 125.00 \
  --discount-percent 10 \
  --no-save

echo ""
echo "7. Testing client report..."
python3 invoice_report.py client demo_client

echo ""
echo "=== All Tests Passed! ==="
echo ""
echo "Generated files:"
ls -lh output/
echo ""
echo "Data files:"
ls -lh data/*.jsonl
