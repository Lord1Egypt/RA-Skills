# StdReport Recipes

## Recipe 1: Standard integrated report page

```tsx
import { CStandardPage, useStandardReport, OrbcafeI18nProvider } from 'orbcafe-ui';

const metadata = {
  id: 'orders-report',
  title: 'Orders',
  columns: [
    { id: 'id', label: 'ID' },
    { id: 'customer', label: 'Customer' },
    { id: 'amount', label: 'Amount', type: 'number', align: 'right' as const },
  ],
  filters: [
    { id: 'keyword', label: 'Keyword', type: 'text' as const },
    {
      id: 'status',
      label: 'Status',
      type: 'select' as const,
      options: [
        { label: 'Active', value: 'active' },
        { label: 'Inactive', value: 'inactive' },
      ],
    },
  ],
};

export default function OrdersPage() {
  const { pageProps } = useStandardReport({
    metadata,
    fetchData: async ({ page, pageSize, filters }) => {
      return {
        rows: [{ id: '1', customer: 'ACME', amount: 1200, status: 'active' }],
        total: 1,
      };
    },
  });

  return (
    <OrbcafeI18nProvider locale="en">
      <CStandardPage {...pageProps} />
    </OrbcafeI18nProvider>
  );
}
```

## Recipe 2: Table-only + quick operations + graph entry

```tsx
import { CTable } from 'orbcafe-ui';

<CTable
  appId="orders-table"
  title="Orders"
  columns={[
    { id: 'id', label: 'ID' },
    { id: 'status', label: 'Status' },
    { id: 'amount', label: 'Amount', numeric: true },
  ]}
  rows={rows}
  rowKey="id"
  selectionMode="multiple"
  graphReport={{ enabled: true, interaction: { enabled: true } }}
  quickCreate={{
    enabled: true,
    title: 'Create Order',
    onSubmit: async (payload) => createOrder(payload),
  }}
  quickEdit={{
    enabled: true,
    onSubmit: async (payload, row) => updateOrder(row.id, payload),
  }}
  quickDelete={{
    enabled: true,
    onConfirm: async (selectedRows) => deleteOrders(selectedRows.map((r) => r.id)),
  }}
/>;
```
