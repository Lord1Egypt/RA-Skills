# QR Code

A QR code for a project link, to print on a menu, flyer, table card or business card, or to show on
screen. The QR encodes the project's public link, so it keeps working when the project gets a new
version (`actions/replace-project.md`): nothing needs reprinting. Paid plans (Starter and up).

## When to use

- "Give me a QR code for this link", "I want to print it on the menu", "QR for my flyer"
- Right after publishing something meant to be printed or used as a bio link

---

## Get the QR code

No request body and no API key: the image URLs only need the `projectId`.

```
https://connect.litehost.io/qr/{projectId}.png   (screens and most printing)
https://connect.litehost.io/qr/{projectId}.svg   (print shops; scales without blur)
```

Give the user both links. To save a copy locally:

```bash
curl -fsS -o litehost-qr.png https://connect.litehost.io/qr/PROJECT_ID.png
```

## Errors

| Status | Meaning | What to do |
|---|---|---|
| 403 `QR codes need a paid plan.` | The owner is on Free | Tell the user and link https://litehost.io/dashboard?upgrade=plans |
| 404 | Unknown, archived or expired project | Check the id with `actions/list-projects.md` |

On Free, a link nobody opens for 90 days is paused, and a printed QR would stop working with it:
say so before the user prints anything.
