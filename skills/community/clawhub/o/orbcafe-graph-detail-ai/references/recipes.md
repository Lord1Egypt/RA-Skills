# Graph + Detail + Agent Recipes

## Recipe 1: Graph report dialog

```tsx
import { CGraphReport } from 'orbcafe-ui';

<CGraphReport
  open={open}
  onClose={onClose}
  model={model}
  tableContent={tableContent}
/>;
```

## Recipe 2: Detail page with search + AI fallback

```tsx
import { CDetailInfoPage } from 'orbcafe-ui';

<CDetailInfoPage
  title="Invoice #INV-001"
  sections={[
    {
      id: 'basic',
      title: 'Basic Info',
      fields: [
        { id: 'invoiceId', label: 'Invoice ID', value: 'INV-001' },
        { id: 'customer', label: 'Customer', value: 'Schunk Intec' },
      ],
    },
  ]}
  tabs={[
    {
      id: 'notes',
      label: 'Notes',
      fields: [{ id: 'owner', label: 'Owner', value: 'Ruiyang' }],
    },
  ]}
  ai={{
    enabled: true,
    onSubmit: async (query) => `### AI Insight\nNo direct field match for **${query}**`,
  }}
/>;
```

## Recipe 3: AI settings dialog

```tsx
import { CCustomizeAgent } from 'orbcafe-ui';

<CCustomizeAgent
  open={open}
  onClose={onClose}
  value={{
    baseUrl: '/llm-api',
    apiKey: '',
    model: 'doubao-lite',
    promptLang: 'zh',
    analysisPrompt: '...',
    responsePrompt: '...',
  }}
  analysisTemplateOptions={[{ id: 'analysis-default', label: 'Default Analysis' }]}
  responseTemplateOptions={[{ id: 'response-default', label: 'Default Response' }]}
  onSaveAll={async ({ settings, analysisTemplateId, responseTemplateId }) => {
    await saveAll({ settings, analysisTemplateId, responseTemplateId });
  }}
/>;
```
