# Layout Patterns

## Pattern 1: Full application shell

```tsx
import { CAppPageLayout } from 'orbcafe-ui';

<CAppPageLayout
  appTitle="ORBCAFE"
  menuData={[{ id: 'std', title: 'Standard Report', href: '/std-report' }]}
  locale="zh"
  user={{ name: 'Ruiyang Shen', subtitle: 'ruiyang.shen@orbis.de' }}
  onUserSetting={() => router.push('/settings')}
  onUserLogout={() => auth.logout()}
>
  <div>Page Content</div>
</CAppPageLayout>;
```

## Pattern 2: Nav-only + custom content orchestration

```tsx
import { NavigationIsland, useNavigationIsland } from 'orbcafe-ui';

const nav = useNavigationIsland({ menuData });

<NavigationIsland
  menuData={menuData}
  collapsed={nav.collapsed}
  onToggleCollapsed={nav.toggleCollapsed}
/>;
```

## Pattern 3: Markdown + transition utility

```tsx
import { MarkdownRenderer, CPageTransition } from 'orbcafe-ui';

<CPageTransition transitionKey={pathname} variant="slide-up" durationMs={220}>
  <MarkdownRenderer markdown={markdownText} />
</CPageTransition>;
```
