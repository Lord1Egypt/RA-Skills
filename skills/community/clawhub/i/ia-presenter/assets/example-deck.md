/assets/cover.jpg
Background: true
filter: darken
opacity: 60%

	A talk about talks
# Say Less, Show Less
### How iA Presenter keeps slides and speech apart

Good morning. This deck is also a syntax sample: every pattern below is verified in iA Presenter 2.0.2. Everything flush-left, like this paragraph, is speaker notes. Only the heading block above is on the slide.

---
### Agenda
	1. Write the story
	2. Cut it into slides
	3. Show only what matters
	4. Design last

A TAB in front of each list item puts the list on the slide. Without the TAB the list would be notes.

---
## 1. Write the story first

Start with the script. Write it like an email to one person in the audience. Don't touch layout yet.

---
## What you say ≠ what you show
	People read at ~250 wpm. You speak at ~110–150.

If the slide says everything, they read ahead and stop listening. Show a hook, say the rest.

---
Layout: Section

## 2. Structure

Three dashes make a slide. One idea per slide. This one uses `Layout: Section` to get the big left-aligned section style.

---
## Cells shape the layout

### Left
	A blank line between blocks makes a new cell.

### Right
	Two or three cells sit side by side. Four or more become a grid.

This slide is a title plus two cells → title row with two columns, chosen automatically.

---
## Compare with a split

/assets/before.jpg
size: contain

/assets/after.jpg
size: contain

Two image cells side by side. `size: contain` avoids cropping.

---
#### Caption on top, image below

/assets/diagram.png
size: contain

An H4 in its own cell before the image becomes the caption. Swap the order to caption below.

---
## Numbers, as a chart
| Quarter | Revenue | Cost |
| :------ | ------: | ---: |
| Q1      | 10      | 6    |
| Q2      | 15      | 8    |
| Q3      | 25      | 12   |
Chart: bar
yLabel: Millions

Tables are visible without a TAB. The `Chart:` line under the table turns it into a bar chart in the theme's colors. Remove the metadata to show the table itself.

---
Class: quote

## "The heart of a great presentation is the message."
#### — iA

A `Class:` line adds a CSS class to this slide, which a custom theme can style.

---
### Details when you need them
	Inline math $E = mc^2$, a footnote[^Verified in iA Presenter 2.0.2.] and ==a highlight==.

```python
def promote(line):
    return "\t" + line   # a TAB makes it visible
```

Code blocks and math are visible by default; the paragraph above needed its TAB.

---
## 4. Design last
	Pick the theme in info.json or the Design tab.

Themes are cities: Tokyo, Paris, New York, Copenhagen… Change one field and every slide re-flows. Never fiddle with boxes.

---
# Show one thing. Say the rest.

Land on a line they can repeat, not on "Thank you".
