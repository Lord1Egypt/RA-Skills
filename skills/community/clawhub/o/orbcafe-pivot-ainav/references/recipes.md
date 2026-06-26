# Pivot + AINav Recipes

## Recipe 1: Controlled pivot table with hook

```tsx
import { CPivotTable, usePivotTable } from 'orbcafe-ui';

const pivot = usePivotTable({
  fields,
  initialLayout: {
    rows: ['region'],
    columns: ['quarter'],
    values: [{ fieldId: 'revenue', aggregation: 'sum' }],
  },
});

<CPivotTable rows={dataRows} fields={fields} model={pivot.model} />;
```

## Recipe 2: Pivot preset management

```tsx
import { CPivotTable, type PivotTablePreset } from 'orbcafe-ui';

const [presets, setPresets] = useState<PivotTablePreset[]>([]);

<CPivotTable
  rows={rows}
  fields={fields}
  enablePresetManagement
  presets={presets}
  onPresetsChange={setPresets}
/>;
```

## Recipe 3: Voice navigation provider

```tsx
import { CAINavProvider } from 'orbcafe-ui';

<CAINavProvider
  onVoiceSubmit={async (text) => {
    await routeByIntent(text);
  }}
  onVoiceError={(err) => console.error(err)}
  longPressMs={200}
  wsUrl="ws://localhost:8765"
>
  {children}
</CAINavProvider>;
```
