# Migration — From Cypress, Puppeteer, or Selenium

Porting is mostly deleting: the waits, the retries, and the plugins that existed to work around the old tool.

## Do Not Port A Bad Suite

Before translating, decide per test: is this still worth its runtime (`testing.md`)? A migration is the cheapest moment to drop tests that assert nothing unique — translating them costs the same and preserves the maintenance bill forever.

Strangler approach: run both suites side by side, port the highest-value journeys first, and delete each old test the day its replacement passes twice in CI. A big-bang rewrite stalls at 60% and leaves two half-suites.

## From Cypress

| Cypress | Playwright | Note |
|---|---|---|
| `cy.get('.btn').click()` | `await page.getByRole('button', { name }).click()` | Every command is awaited; no implicit chain queue |
| `cy.contains('Save')` | `page.getByText('Save')` | Playwright's is substring + case-insensitive by default |
| `cy.wait(500)` | Delete it | Assertions retry (`waiting.md`) |
| `cy.wait('@alias')` | `page.waitForResponse('**/api/x')` | Register **before** the trigger |
| `cy.intercept()` | `page.route()` | `network.md` |
| `cy.request()` | `request` fixture or `page.request` | Different cookie jars — see `network.md` |
| `cy.session()` | `storageState` + setup project | `auth.md` |
| Custom commands | Fixtures | Typed, scoped, with teardown |
| `cy.task()` | Plain Node in a fixture | No IPC boundary; you are already in Node |
| `.should('be.visible')` | `await expect(locator).toBeVisible()` | |
| `cypress-file-upload` plugin | `setInputFiles` | Built in |
| `cypress-iframe` plugin | `frameLocator` | Built in |
| `Cypress.env()` | `process.env` | |

Habits to unlearn:

- **The queue.** Cypress commands enqueue; Playwright statements execute when awaited. A forgotten `await` produces a test that passes while doing nothing — enable the `no-floating-promises` lint rule on day one.
- **One tab, one origin.** Playwright handles multiple tabs, windows, and origins natively (`contexts.md`); flows that were split in two to work around Cypress can be rejoined.
- **Retry-ability of a chain.** In Playwright the retrying unit is the assertion, not the chain: `expect(locator)` retries, `await locator.textContent()` does not.
- **`beforeEach` state reset.** Playwright gives a fresh context per test automatically; the manual clearing is redundant.

## From Puppeteer

Playwright's API descends from Puppeteer, so most code compiles after renaming — which is the trap: it runs, and it keeps every manual wait.

| Puppeteer | Playwright |
|---|---|
| `page.$('.sel')`, `page.$$` | Locators — no handles, auto-waiting |
| `page.waitForSelector('.sel')` then act | Just act; the locator waits |
| `page.waitForTimeout(1000)` | An assertion on the state |
| `page.click('.sel')` | `page.getByRole(...).click()` |
| `browser.createIncognitoBrowserContext()` | `browser.newContext()` — always isolated |
| `page.setViewport()` | `page.setViewportSize()` or context options |
| `page.type()` | `locator.fill()` (instant) or `locator.pressSequentially()` (per key) |
| Manual `waitForNavigation` around a click | Assert the destination |

Real gains beyond syntax: three engines instead of one, the trace viewer, the test runner with fixtures and retries, and the strict-mode error that catches ambiguous selectors your Puppeteer code silently resolved to the first match.

## From Selenium

| Selenium | Playwright |
|---|---|
| Implicit/explicit waits, `WebDriverWait` | Auto-waiting per action |
| `By.xpath(...)` | Role, label, text locators |
| `StaleElementReferenceException` | Structurally impossible — locators re-resolve |
| Selenium Grid | Sharding across CI machines (`ci-cd.md`) |
| Page Factory | Page objects or fixtures (`fixtures.md`) |
| Driver binary management | Browsers ship with the package (`browsers.md`) |

Selenium suites usually carry a homemade wait helper wrapping everything. Delete it in the port; keeping it reintroduces the polling Playwright already does, with worse error messages. Expect the biggest wins here: a Selenium suite ported straight across typically loses its whole `StaleElementReference` retry layer.

## Porting Checklist Per Test

- [ ] Every action awaited, no floating promises
- [ ] No `wait(ms)` survived the port
- [ ] Locators rewritten to role/label/text — not the old XPath transliterated
- [ ] Assertions are web-first (`expect(locator)`, not `expect(await ...)`)
- [ ] Setup moved to a fixture; no shared mutable account (`fixtures.md`, `auth.md`)
- [ ] Login goes through `storageState`, not the UI, unless login is the test
- [ ] Passes `--repeat-each=10 --workers=4` before the old test is deleted
