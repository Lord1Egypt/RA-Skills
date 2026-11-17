Target file: `article.md`

```md
# A reusable content workflow

![Cover](./images/cover.png)

<img src="./images/diagram.png" alt="workflow diagram">

![Architecture][arch]

[arch]: ./images/architecture.png "architecture"

![Existing](https://img.example.com/already-public.png)
```

Run the first inspection without external writes:

```bash
./run.sh article.md
```

For a reviewed local replacement test, create `replacements.json`:

```json
{
  "./images/cover.png": "https://img.example.com/md-assets/cover.png",
  "./images/diagram.png": "https://img.example.com/md-assets/diagram.png",
  "./images/architecture.png": "https://img.example.com/md-assets/architecture.png"
}
```

Then apply only after reviewing that map:

```bash
./run.sh article.md --apply --confirm-write --url-map replacements.json
```
