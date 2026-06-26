# k6 Advanced Patterns

## Parameterized Data (CSV)

```javascript
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';
import { SharedArray } from 'k6/data';

const users = new SharedArray('users', function () {
  return papaparse.parse(open('./users.csv'), { header: true }).data;
});

export default function () {
  const user = users[__VU % users.length];
  http.post(`${BASE_URL}/login`, JSON.stringify({
    username: user.username,
    password: user.password,
  }), { headers: { 'Content-Type': 'application/json' } });
}
```

## Scenarios (Multiple User Profiles)

```javascript
export const options = {
  scenarios: {
    browse: {
      executor: 'constant-vus',
      vus: 50,
      duration: '10m',
      exec: 'browseFlow',
    },
    purchase: {
      executor: 'ramping-arrival-rate',
      startRate: 1,
      timeUnit: '1s',
      preAllocatedVUs: 50,
      stages: [
        { duration: '5m', target: 10 },
        { duration: '5m', target: 10 },
      ],
      exec: 'purchaseFlow',
    },
  },
};

export function browseFlow() {
  http.get(`${BASE_URL}/products`);
  sleep(2);
  http.get(`${BASE_URL}/products/${Math.floor(Math.random() * 100)}`);
  sleep(1);
}

export function purchaseFlow() {
  const item = http.get(`${BASE_URL}/products/1`).json();
  http.post(`${BASE_URL}/cart`, JSON.stringify({ productId: item.id }));
  http.post(`${BASE_URL}/checkout`, JSON.stringify({ cartId: 'test' }));
}
```

## Browser-based Testing (k6 browser module)

```javascript
import { browser } from 'k6/browser';

export const options = {
  scenarios: {
    ui: {
      executor: 'constant-vus',
      vus: 5,
      duration: '2m',
      options: { browser: { type: 'chromium' } },
    },
  },
};

export default async function () {
  const page = await browser.newPage();
  await page.goto('https://app.example.com');
  await page.locator('#username').fill('test');
  await page.locator('#password').fill('pass');
  await page.locator('button[type=submit]').click();
  await page.waitForNavigation();
  page.close();
}
```

## Thresholds by Group

```javascript
import { group } from 'k6';

export const options = {
  thresholds: {
    'group_duration{group:::Auth}': ['p(95)<2000'],
    'group_duration{group:::Browse}': ['p(95)<500'],
    'http_req_duration{name:login}': ['p(99)<3000'],
  },
};

export default function () {
  group('Auth', function () {
    http.post(`${BASE_URL}/login`, payload, { tags: { name: 'login' } });
  });
  group('Browse', function () {
    http.get(`${BASE_URL}/items`);
  });
}
```
