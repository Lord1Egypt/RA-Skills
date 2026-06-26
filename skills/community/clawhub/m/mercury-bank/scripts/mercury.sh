#!/usr/bin/env bash
# Mercury API helper script
# Usage: mercury.sh <command> [args]
# Commands: accounts, account, balance, transactions, transaction,
#           invoices, invoice, create-invoice, cancel-invoice,
#           customers, customer, create-customer, recipients, org

set -euo pipefail

SECRETS_FILE="${HOME}/.secrets/mercury.env"
if [ -f "$SECRETS_FILE" ]; then
  source "$SECRETS_FILE"
fi

TOKEN="${MERCURY_API_TOKEN:-}"
BASE="https://api.mercury.com/api/v1"

if [ -z "$TOKEN" ]; then
  echo "ERROR: MERCURY_API_TOKEN not set. Add to ~/.secrets/mercury.env" >&2
  exit 1
fi

call() {
  local method="$1"; shift
  local path="$1"; shift
  local data="${1:-}"

  if [ -n "$data" ]; then
    curl -s --user "$TOKEN:" \
      -X "$method" \
      -H "Content-Type: application/json" \
      -d "$data" \
      "${BASE}${path}"
  else
    curl -s --user "$TOKEN:" -X "$method" "${BASE}${path}"
  fi
}

CMD="${1:-help}"
shift || true

case "$CMD" in
  accounts)
    call GET /accounts | python3 -m json.tool
    ;;
  account)
    ID="${1:-4ca92254-e020-11f0-ab61-779167c16d40}"
    call GET "/account/$ID" | python3 -m json.tool
    ;;
  balance)
    call GET /accounts | python3 -c "
import json, sys
data = json.load(sys.stdin)
for a in data.get('accounts', []):
    print(f\"{a['name']}: \${a['availableBalance']:,.2f} available\")
"
    ;;
  transactions)
    ACCOUNT="${1:-4ca92254-e020-11f0-ab61-779167c16d40}"
    LIMIT="${2:-20}"
    call GET "/account/$ACCOUNT/transactions?limit=$LIMIT" | python3 -m json.tool
    ;;
  transaction)
    call GET "/transaction/$1" | python3 -m json.tool
    ;;
  invoices)
    call GET /ar/invoices | python3 -m json.tool
    ;;
  invoice)
    call GET "/ar/invoices/$1" | python3 -m json.tool
    ;;
  create-invoice)
    # Args: customer_id amount_cents due_date memo [invoice_number]
    CUSTOMER_ID="$1"
    AMOUNT="$2"
    DUE_DATE="$3"
    MEMO="${4:-}"
    INV_NUM="${5:-}"
    TODAY=$(date +%Y-%m-%d)

    # Auto-increment invoice number if not provided
    if [ -z "$INV_NUM" ]; then
      LAST=$(call GET /ar/invoices | python3 -c "
import json, sys, re
data = json.load(sys.stdin)
nums = []
for inv in data.get('invoices', []):
    m = re.search(r'INV-(\d+)', inv.get('invoiceNumber',''))
    if m: nums.append(int(m.group(1)))
print(max(nums)+1 if nums else 1)
")
      INV_NUM="INV-$LAST"
    fi

    PAYLOAD=$(python3 -c "
import json
d = {
    'invoiceNumber': '$INV_NUM',
    'invoiceDate': '$TODAY',
    'dueDate': '$DUE_DATE',
    'customerId': '$CUSTOMER_ID',
    'destinationAccountId': '4ca92254-e020-11f0-ab61-779167c16d40',
    'amount': $AMOUNT,
    'achDebitEnabled': True,
    'creditCardEnabled': False
}
if '$MEMO': d['payerMemo'] = '$MEMO'
print(json.dumps(d))
")
    call POST /ar/invoices "$PAYLOAD" | python3 -m json.tool
    ;;
  cancel-invoice)
    call POST "/ar/invoices/$1/cancel" '{}' | python3 -m json.tool
    ;;
  customers)
    call GET /ar/customers | python3 -m json.tool
    ;;
  customer)
    call GET "/ar/customers/$1" | python3 -m json.tool
    ;;
  create-customer)
    # Args: name email address1 city region postalcode country
    PAYLOAD=$(python3 -c "
import json, sys
d = {
    'name': sys.argv[1],
    'email': sys.argv[2],
    'address': {
        'address1': sys.argv[3],
        'city': sys.argv[4],
        'region': sys.argv[5],
        'postalCode': sys.argv[6],
        'country': sys.argv[7]
    }
}
print(json.dumps(d))
" "$1" "$2" "$3" "$4" "$5" "$6" "${7:-US}")
    call POST /ar/customers "$PAYLOAD" | python3 -m json.tool
    ;;
  recipients)
    call GET /recipients | python3 -m json.tool
    ;;
  org)
    call GET /organization | python3 -m json.tool
    ;;
  help|*)
    echo "Mercury API CLI"
    echo ""
    echo "Commands:"
    echo "  accounts                          List all accounts"
    echo "  account [id]                      Get account (default: Checking)"
    echo "  balance                           Show balances for all accounts"
    echo "  transactions [account_id] [limit] List transactions"
    echo "  transaction <id>                  Get transaction by ID"
    echo "  invoices                          List all AR invoices"
    echo "  invoice <id>                      Get invoice by ID"
    echo "  create-invoice <customer_id> <amount_cents> <due_date> [memo] [inv_num]"
    echo "  cancel-invoice <id>               Cancel an invoice"
    echo "  customers                         List AR customers"
    echo "  customer <id>                     Get customer by ID"
    echo "  create-customer <name> <email> <addr> <city> <region> <zip> [country]"
    echo "  recipients                        List payment recipients"
    echo "  org                               Get organization details"
    ;;
esac
