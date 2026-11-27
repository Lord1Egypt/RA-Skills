# Character sheet and cover prompts

Replace the parts in angle brackets with fields from the plan. These are the prompts Musikalis Story MV uses for the same images. They work with image models that take reference images.

## Character sheet from a photo

Send the user's photo as the reference image.

```text
Character reference sheet of the person in the reference photo, same face, hair and skin tone.
Layout on one plain light grey background: on the left a large head-and-shoulders portrait; on the right three full-body views of the same person standing — front, side, back — at the same scale.
Appearance: <character.appearance>
Wardrobe (identical in every view): <character.wardrobe>
Style: <visualStyle>
Even studio lighting, sharp details, no text, no labels, no extra people.
```

Draw the supporting character the same way, with their own photo and the `supporting` fields.

## Character sheet from a description

For a character with no photo.

```text
Character reference sheet of one original adult character.
Layout on one plain light grey background: on the left a large head-and-shoulders portrait; on the right three full-body views of the same character standing — front, side, back — at the same scale.
Character: <a description of up to 500 characters: look, clothes, art style>
One outfit, identical in every view. Follow any art style in the description; otherwise photorealistic.
Even studio lighting, sharp details, no text, no labels, no extra people.
```

## Cover

Reference image 1 is the main character's sheet or photo. Reference image 2, if there is one, is the supporting character's.

```text
Music video cover art. <coverPrompt>
The main character is the person in reference image 1: <character.appearance>; wearing <character.wardrobe>.
The supporting character is the person in reference image 2: <supporting.appearance>; wearing <supporting.wardrobe>.
Style: <visualStyle>
Leave clean space for the title "<title>" and render that title as elegant large lettering that fits the style; no other text.
```

With one character, drop the supporting line and write "the person in the reference image" in the main character line. For a cover without lettering, replace the last line with `No text.`

## Tips

- Redraw the sheet until the face matches the photo before you make any video. Every clip copies the sheet, mistakes included.
- Keep the wardrobe text word for word the same in the sheet, the cover and every shot.
- One sheet works for both 16:9 and 9:16 videos.
