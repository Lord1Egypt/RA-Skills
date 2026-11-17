# Files — Uploads, Downloads, PDFs, and Clipboard

File flows fail for one reason: the browser event is asynchronous and the test acts after it fired. Register the waiter first, always.

## Uploads

```typescript
await page.getByLabel('Avatar').setInputFiles('fixtures/avatar.png');
await page.getByLabel('Attachments').setInputFiles(['a.pdf', 'b.pdf']);   // multiple
await page.getByLabel('Avatar').setInputFiles([]);                        // clear the input

// In-memory file, no fixture on disk
await page.getByLabel('CSV').setInputFiles({
  name: 'data.csv', mimeType: 'text/csv', buffer: Buffer.from('id,name\n1,Alice'),
});
```

- `setInputFiles` targets the `<input type="file">` itself, and it works even when the input is **hidden** behind a styled button — the usual mistake is locating the pretty button instead of the input.
- No visible input at all (drag-drop zones, custom pickers): intercept the chooser.

```typescript
const chooserPromise = page.waitForEvent('filechooser');
await page.getByRole('button', { name: 'Upload' }).click();
const chooser = await chooserPromise;
await chooser.setFiles('fixtures/report.pdf');
```

- Assert the **result**, not the call: `await expect(page.getByText('avatar.png')).toBeVisible()`. `setInputFiles` resolving proves nothing about the upload.
- Large files: the upload request is a real request — wait for its response, not a fixed delay.
- Fixture paths are resolved relative to the current working directory; use `path.join(__dirname, 'fixtures', ...)` so the test survives being run from the repo root or its own folder.

## Drag And Drop Of Files

HTML5 drop zones need a synthetic `DataTransfer`:

```typescript
const dataTransfer = await page.evaluateHandle(async () => {
  const dt = new DataTransfer();
  dt.items.add(new File(['id,name\n1,Alice'], 'data.csv', { type: 'text/csv' }));
  return dt;
});
await page.getByTestId('dropzone').dispatchEvent('drop', { dataTransfer });
```

Element-to-element dragging is different and simpler: `await source.dragTo(target)`. When a drag library needs intermediate movement, drive it manually — `mouse.down()`, two or three `mouse.move()` steps, `mouse.up()` — because most libraries ignore a single jump.

## Downloads

```typescript
const downloadPromise = page.waitForEvent('download');
await page.getByRole('button', { name: 'Export CSV' }).click();
const download = await downloadPromise;

expect(download.suggestedFilename()).toBe('report.csv');
const stream = await download.createReadStream();          // assert content without touching disk
await download.saveAs(test.info().outputPath('report.csv'));
```

- Downloads live in a temp dir and are **deleted when the context closes** unless saved. `saveAs` into `testInfo.outputPath` puts them next to the test's other artifacts and cleans up with them.
- `acceptDownloads` is on by default; turning it off makes downloads fail rather than pause.
- `download.path()` waits for the transfer to finish — use it (or the stream) before asserting size or content.
- Some apps download by navigating to a URL that responds with `Content-Disposition`. If nothing fires, check whether the click opened a new tab: listen on the context, not the page.
- Faster and more precise for content assertions: get the URL from the button, then `page.request.get(url)` and assert on the response body. The browser only needs to prove the link is right.

## PDFs

```typescript
await page.pdf({ path: 'out.pdf', format: 'A4', printBackground: true });
```

- **Chromium headless only.** Firefox, WebKit, and headed Chromium throw.
- `page.pdf` renders the print stylesheet, not the screen: `await page.emulateMedia({ media: 'print' })` first if you want to see what you are generating.
- Asserting a generated PDF: check byte length and page count with a parser, or render to an image and compare visually (`visual.md`). Comparing raw PDF bytes fails on embedded timestamps.

## Clipboard

```typescript
await context.grantPermissions(['clipboard-read', 'clipboard-write']);   // Chromium
await page.getByRole('button', { name: 'Copy link' }).click();
const text = await page.evaluate(() => navigator.clipboard.readText());
expect(text).toContain('/share/');
```

Clipboard permissions are Chromium-specific; in Firefox and WebKit, assert the visible confirmation ("Copied!") and cover the copied value in a unit test instead. Keyboard paste (`Meta+V` / `Control+V`) also depends on the platform modifier — read it from `process.platform` or use `ControlOrMeta`.

## File System Boundaries

- Write only into `test.info().outputPath(...)` or the system temp dir. Never into the user's home, never into `~/Clawic/data/playwright/`.
- Generated fixtures belong in `.gitignore`; committed fixtures stay small and are checked for real content (a 0-byte PNG passes an upload and fails an assertion later).
- Clean up in fixture teardown, after `use()`, so it runs even when the test fails.
