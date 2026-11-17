# The material world catalog

Forty worlds, drawn by external assignment. A model's own ranking is a deterministic function of its
priors, so ranking harder cannot beat the prior. This file is the outside source. Read `HOW TO ASSIGN`
at the end before using any entry.

Every world here is a real artifact a person can hold or visit. Every TELL is buildable in CSS or
canvas. Every TYPE pairing is obtainable from Google Fonts or npm.

---

## Print and publishing

### 01. Penguin tri-band paperback
SOURCE     Penguin Books paperback, the horizontal tri-band cover and Tschichold's 1947 Composition Rules
SURFACE    uncoated 250 gsm board, letterpress ink sunk slightly into the stock, aged to cream
STRUCTURE  three horizontal bands, top and bottom coded by series, the centre band white and carrying the title
TYPE       `EB Garamond` (text) + `Cabin` (titling, Gill and Johnston lineage)
COLOR      #E8E2D0 cream, #FF6F1F fiction orange, #14713D crime green, #1B1B1A ink
MOTION     section changes as a horizontal band wipe at 240ms. Nothing else moves
TELL       band edges are hard with zero radius, and band height is always a whole multiple of the line height

### 02. Whole Earth Catalog
SOURCE     Stewart Brand's Whole Earth Catalog, 1968, oversized newsprint pages of reviewed tools
SURFACE    groundwood newsprint, one-colour offset, 65 lpi halftone dots visible, show-through from the reverse
STRUCTURE  three ragged columns of dense reviews, each item carrying a price, a supplier and an address
TYPE       `Courier Prime` (reviews) + `Archivo` (headings)
COLOR      #D9D2C2 newsprint, #2B2A26 ink, #8C4A2F rust second colour, #6E6A5E halftone grey
MOTION     nothing animates. New items append to a column and the column reflows
TELL       every item carries a price and a supplier in the same fixed position, and photographs get a real halftone via a CSS mask rather than a filter

### 03. Twen magazine
SOURCE     Twen, art directed by Willy Fleckhaus from 1959, built on a twelve-column grid
SURFACE    coated stock, deep gravure blacks, photographs printed to the trim with no margin
STRUCTURE  the grid used at both extremes: one image across all twelve columns, then body text in a single column with enormous white gutters
TYPE       `Tinos` (headlines, Times metrics) + `Archivo Black` (folios and numerals)
COLOR      #0B0B0B black, #F2F0EB paper, #D8232A red, #C7B37F ochre
MOTION     images scale within a fixed frame on scroll, by at most 4 percent
TELL       exactly one image is allowed to break the grid and bleed off three edges; every other element snaps to the twelve columns with no exception

### 04. Type foundry specimen book
SOURCE     an American Type Founders specimen book showing one face at every size the foundry casts
SURFACE    heavy laid paper, letterpress impression visible as debossing, ink squash at the letter edges
STRUCTURE  one face per spread at 6, 8, 10, 12, 18, 24, 36, 48 and 72 point in descending blocks
TYPE       `IM Fell English` (the specimen face) + `Archivo Black` (size numerals in the margin)
COLOR      #EFE9DC paper, #1A1714 ink, #A32D25 second colour, #7A7263 rule grey
MOTION     scrolling steps the display through its size ladder in discrete jumps, never a smooth scale
TELL       every block prints its own point size and its measured characters per line in the margin, and the ladder is a real one

### 05. Agate stock tables
SOURCE     the share listings on a broadsheet financial page, set in 5.5 point agate
SURFACE    newsprint, tight register, hairline rules occasionally broken by the press
STRUCTURE  fixed columns (name, high, low, close, change, volume) repeated in five vertical stacks per page, alphabetical, no interior headings
TYPE       `Roboto Condensed` (names) + `Azeret Mono` (figures, tabular numerals)
COLOR      #E4E0D6 stock, #14140F ink, #B03A2E down, #1E6B3A up
MOTION     only a changed cell flashes its direction colour for 400ms, then returns
TELL       tabular lining figures at a fixed column width, so no row shifts when a value changes digit count

### 06. Museum wall label
SOURCE     a curatorial object label beside a case, and the object file it is drawn from
SURFACE    2 mm matte-laminated board mounted 3 mm off the wall, soft shadow under a raking gallery light
STRUCTURE  maker, dates, title in italic, date of work, materials, dimensions, accession number, credit line, always in that order and always left aligned
TYPE       `Source Serif 4` (title, italic) + `Public Sans` (label body, 11 px floor)
COLOR      #F4F2ED board, #22201C text, #8A8578 secondary, #B4A05F credit line
MOTION     labels do not move. Hovering the object raises its label 2 px and deepens the cast shadow
TELL       every object carries an accession number, in the same position at the same size, even when it is the least interesting thing on the label

---

## Showcard and ephemera

### 07. Boxing fight poster
SOURCE     a wood-type fight bill: main event, undercard, venue, date, promoter's mark
SURFACE    cheap poster stock, wood type printed with visible ink starvation on the largest characters, two spot colours
STRUCTURE  a strict vertical hierarchy of size with no columns: main event, VS, descending undercard tiers, then a solid band with venue and doors time
TYPE       `Alfa Slab One` (main event) + `Barlow Condensed` (undercard) + `Archivo Black` (the band)
COLOR      #F2E7C9 stock, #101010 ink, #C8102E red, #F2B705 yellow
MOTION     tiers arrive already stacked. One element only, the VS, scales once on load
TELL       type is set to fill the measure exactly at every tier, so line length drives size rather than the reverse, and tiers are divided by rules of decreasing weight

### 08. Seed packet
SOURCE     a garden seed packet from a rack: chromolithograph front, sowing data on the reverse
SURFACE    uncoated kraft-toned paper with a glued side seam, lithographed face, letterpress reverse
STRUCTURE  front carries the illustration and the variety name only; the reverse carries the entire data model in small type
TYPE       `Zilla Slab` (variety name) + `Cutive Mono` (the reverse data)
COLOR      #E9DCC0 kraft, #2F4A2C leaf, #B8452F vermilion, #1C1B18 ink, #D9A441 gold
MOTION     the packet flips: one rotateY at 420ms, and the reverse carries every specification
TELL       sowing depth, spacing, days to germinate, harvest window and packed-for year all exist on the reverse and nowhere else

### 09. Delicatessen ticket and now-serving display
SOURCE     the numbered ticket roll in a chrome dispenser and the seven-segment "now serving" display above a counter
SURFACE    perforated ticket stock, a chrome dispenser, a red LED display on a steel bracket
STRUCTURE  one number owns the display, the queue is implicit, everything else is counter signage priced per 100 grams
TYPE       `Doto` (the display, dot-matrix variable) + `Archivo Black` (counter signage)
COLOR      #1A1A1A body, #FF2D16 LED red, #E8E4D9 ticket stock, #B9BDC0 chrome
MOTION     the number advances by exactly one, with a 60ms flicker as segments switch. Never a tween
TELL       the ticket the visitor holds stays visible on screen while the served number moves, so the distance between them is the state

---

## Industrial and manufacturing

### 10. 1970s parts microfiche catalogue
SOURCE     a manufacturer parts catalogue on microfiche: exploded assembly plates keyed to part numbers
SURFACE    microfilm on a backlit reader, optical vignette at the corners, high-contrast line art on a warm white field
STRUCTURE  exploded isometric diagram left with numbered balloons, fixed-width table right mapping balloon to part number, description, quantity and model applicability
TYPE       `IBM Plex Mono` (part numbers and table) + `Barlow Condensed` (diagram callouts)
COLOR      #F5F2E8 field, #16150F line, #9A8F72 vignette, #B03A2E supersession note
MOTION     diagram pans and zooms as one unit; hovering a table row highlights its balloon and nothing else
TELL       balloons and table rows are linked in both directions, and every superseded part carries its supersession note

### 11. Braun control panel
SOURCE     the front panel of a Braun appliance designed by Rams and Gugelot: SK4, T3, ET66
SURFACE    bead-blasted aluminium and matte off-white ABS, controls sunk into a recess with a crisp 0.5 mm shadow line
STRUCTURE  functions in a grid of equal cells, every control the same size unless importance genuinely differs, labels below the control and never inside it
TYPE       `Schibsted Grotesk` (labels) + `Roboto Mono` (values)
COLOR      #EDEBE6 shell, #2A2A28 graphite, #F2A20C signal yellow, #1F6B3F green, #C4C7C5 aluminium
MOTION     controls travel: a button depresses 1 px and its shadow shortens, a dial rotates to a detent and stops hard
TELL       exactly one control on the surface is yellow, it starts the process, and no other element anywhere on the page may use that hue

### 12. Heavy equipment service manual
SOURCE     a Caterpillar or Deere service manual: procedures, torque tables, exploded views, safety triangles
SURFACE    oil-resistant coated paper in a ring binder, corners softened by use, a thumbprint in the outer margin
STRUCTURE  numbered procedures each preceded by a specification block, torque values tabled with units and tolerance, warnings boxed with a triangle
TYPE       `Archivo Narrow` (procedures) + `IBM Plex Mono` (specifications and torque tables)
COLOR      #EAE7DE paper, #1C1B17 ink, #F2C200 machine yellow, #9E2A17 warning red, #6A665A rule
MOTION     steps expand in place and push the next step down. Nothing overlays anything
TELL       every numeric specification carries its unit and its tolerance in the same cell, and the tolerance is never dropped for tidiness

### 13. Machine shop job traveller
SOURCE     the card that follows a part through a machine shop, stamped at each operation
SURFACE    manila card stock punched for a rack, typewriter impression, rubber-stamped ink of uneven saturation, ballpoint initials
STRUCTURE  a table of operations down the card: op number, machine, setup, tooling, quantity, operator, date, inspection stamp. The card accumulates and is never rewritten
TYPE       `Special Elite` (typewriter body) + `Archivo Narrow` (pre-printed form labels)
COLOR      #DCCFAE manila, #1F1D1A type, #2B4A8C stamp blue, #A02B1F reject red
MOTION     a stamp lands: one scale-and-settle at 180ms with a different rotation offset each time
TELL       pre-printed rules and typed content are visibly different inks, and every completed operation carries an operator initial and a date that were not there before

### 14. Cyanotype blueprint
SOURCE     an engineering blueprint: white line on Prussian blue, contact printed
SURFACE    coated paper with an uneven blue wash, lighter where the coating thinned, occasional fixing stains
STRUCTURE  a title block bottom right (drawing number, scale, revision, drawn by, checked by) and a border carrying zone letters and numbers
TYPE       `Architects Daughter` (annotations) + `Cousine` (title block and dimensions)
COLOR      #10305C blue, #E9EEF5 line white, #0A1F3D shadow, #C8D4E3 wash edge
MOTION     lines draw once on mount via stroke-dashoffset over 900ms, and never again
TELL       the title block is complete including a revision letter and date, and the border zone references are real and cited by other elements

---

## Logistics, transport and navigation

### 15. Shipping manifest and bill of lading
SOURCE     a container bill of lading and the stowage manifest that travels with it
SURFACE    multipart carbonless form, the second copy offset and lighter, dot matrix impact print with visible pin dots
STRUCTURE  a party header (shipper, consignee, notify), then a line-item table of marks, packages, description, gross weight and measurement, then totals at the foot
TYPE       `Courier Prime` (impact print) + `Archivo Narrow` (pre-printed form)
COLOR      #E6E2D4 form, #1A1915 print, #C6BFA8 carbon copy, #1E5C8A form blue, #A8321F stamp
MOTION     rows print left to right at 30ms per column group, like an impact head crossing the page
TELL       totals appear twice, as figures and written out in words, and container numbers are formatted to their real ISO 6346 shape

### 16. Airport departure board
SOURCE     a Solari di Udine split-flap departure board in a terminal hall
SURFACE    matte black flap modules in an aluminium frame, each flap catching hall light differently at the fold line
STRUCTURE  fixed columns of time, destination, flight, gate and remarks, sorted by time, with the remark column carrying the only variable language on the board
TYPE       `Barlow Semi Condensed` (destinations) + `Archivo` (times and gates)
COLOR      #121212 board, #F0EDE4 flap face, #F2B705 amber remark, #3FA34D boarding, #C9302C final call
MOTION     characters cycle through intermediate glyphs to their target at 35ms per step, staggered by column, settling inside 900ms
TELL       a character never fades or slides, and the horizontal fold line across the middle of every glyph is drawn

### 17. Admiralty nautical chart
SOURCE     a British Admiralty chart: soundings, depth contours, lights, a compass rose with magnetic variation
SURFACE    heavy chart paper, four-colour print, folded on a grid, pencil bearings still faintly visible
STRUCTURE  land is buff and nearly empty, water carries every datum, contours nest inward, the title block sits in an empty stretch of sea
TYPE       `EB Garamond` (italic for water features, upright for land) + `Archivo Narrow` (soundings)
COLOR      #F3E7C9 land buff, #DDEAF2 shoal, #F7FAFC deep water, #1B3A5C ink, #C2185B light magenta
MOTION     nothing on the chart moves. Panning is 1:1 with the pointer, with no inertia
TELL       depth figures sit bare in the water with no boxes or pins, and the italic-water, upright-land distinction is honoured on every single label

### 18. Beck's Underground diagram
SOURCE     Harry Beck's 1933 diagram of the London Underground, an electrical schematic applied to a city
SURFACE    a folded pocket card, flat print, line weights uniform regardless of route length
STRUCTURE  every line runs at 0, 45 or 90 degrees only, distance is discarded, stations are ticks, interchanges are circles, the centre is expanded and the outskirts compressed
TYPE       `Cabin` (station names, Johnston lineage) + `IBM Plex Mono` (line codes)
COLOR      #E32017 red, #003688 blue, #00782A green, #FFD300 yellow, #F5F3EC card
MOTION     a route traces along its line at a constant pixel rate, so a longer route genuinely takes longer
TELL       no angle other than 0, 45 or 90 degrees exists anywhere on the page, including in rules, borders and the layout grid itself

### 19. Aircraft quick reference handbook
SOURCE     the QRH in a cockpit: memory items, normal checklists and non-normal procedures
SURFACE    laminated tabbed cards on a ring, matte to kill glare, thumb-worn at the tab edges
STRUCTURE  challenge left and response right, joined by a leader of dots; memory items boxed at the top; conditional branches indented once and never twice
TYPE       `B612` (headings, drawn for cockpit legibility) + `B612 Mono` (challenge and response)
COLOR      #101418 card, #E8EAE6 text, #F2A20C caution amber, #C6382F warning red, #4DA167 normal green
MOTION     a completed item dims to 45 percent and the next item's leader dots brighten. No other motion exists
TELL       the leader dots are real, built from a repeating gradient that recomputes on resize, and the response column never wraps

---

## Scientific and measurement

### 20. Chemistry lab notebook
SOURCE     a bound laboratory notebook with pre-numbered pages and a witness signature line
SURFACE    5 mm quadrille paper, hard-bound so pages cannot be removed, ballpoint pressure visible, one coffee ring
STRUCTURE  date and objective at the top of every page, observations left and calculations right, errors struck through with a single line and initialled, signed and witnessed at the foot
TYPE       `Caveat` (handwritten entries) + `IBM Plex Mono` (printed rules, page numbers, formulae)
COLOR      #F7F4E9 paper, #C9D6C4 grid green, #1B2A6B ink blue, #1F1E1B print, #A83226 correction red
MOTION     nothing animates. Entries append at the foot of the current page and the page number increments
TELL       mistakes are struck through with a single rule and left readable, never deleted, and every page carries a witness line whether or not it is signed

### 21. Oscilloscope front panel
SOURCE     the front of a Tektronix 465: a graticule screen surrounded by grouped, labelled controls
SURFACE    textured grey-blue painted steel, screen-printed legends, a phosphor screen behind an etched graticule
STRUCTURE  controls grouped into bordered regions with a group heading, values printed radially around each knob, the graticule 8 by 10 divisions with minor ticks on the centre axes
TYPE       `Barlow Condensed` (panel legends) + `Share Tech Mono` (readouts)
COLOR      #3A4249 panel, #C8CEC9 legend, #12FF6E phosphor, #0B1210 screen, #E0A21B function amber
MOTION     one continuous trace sweeps at a fixed rate, with phosphor persistence rendered as a fading trail
TELL       the graticule is exactly 8 by 10 divisions with ticks at 0.2 division on the centre lines, and every value is stated in divisions before it is stated in units

### 22. Barograph drum chart
SOURCE     a weekly barograph: an inked arm drawing atmospheric pressure onto a chart wrapped around a clock-driven drum
SURFACE    pre-printed chart paper held on a curve, ink laid by a nib so weight varies with speed, a smudge where the arm was lifted
STRUCTURE  time along the horizontal in days and hours, pressure on a curved vertical scale, the trace crossing the whole week as one unbroken line
TYPE       `Spectral` (scale labels) + `Cutive Mono` (readings)
COLOR      #F1E6D0 chart, #7A2E22 chart rules, #14130F ink trace, #B39B6A drum brass
MOTION     the trace advances at a constant rate left to right and never redraws what it has already drawn
TELL       the vertical scale lines are genuinely curved, drawn as arcs matching the drum radius, not as straight lines

### 23. Slide rule
SOURCE     a Faber-Castell 2/83N: engraved logarithmic scales on a celluloid-faced rule with a glass cursor
SURFACE    cream celluloid over mahogany, divisions engraved and ink-filled, a glass cursor carrying a hairline
STRUCTURE  parallel scales stacked and labelled at the left edge (A, B, C, D, K, L, S, T), divisions unevenly spaced because they are logarithmic, the cursor crossing all of them at once
TYPE       `PT Sans Narrow` (scale labels) + `Cutive Mono` (numerals)
COLOR      #F0E9D6 celluloid, #1C1A16 engraving, #A8231C cursor red, #6B4A2A mahogany, #D9D3C4 slide
MOTION     the slide drags with no easing, because the object has none, and the hairline tracks the pointer exactly
TELL       divisions are computed logarithmically rather than spaced evenly, so a value's position on the page is genuinely its logarithm

### 24. Topographic survey sheet
SOURCE     an Ordnance Survey or Deutsche Grundkarte sheet at 1:25,000 with contours and benchmarks
SURFACE    matte map paper, five-colour offset, contours in orange-brown, a fine blue grid overprinted
STRUCTURE  a bordered sheet with a marginal legend, a grid reference system, a declination diagram, a revision date in the margin, and index contours thickened every fifth line
TYPE       `Barlow Semi Condensed` (place names) + `Space Mono` (grid references and spot heights)
COLOR      #F6F1E4 sheet, #B5652A contour, #2E6E4F woodland, #4A6FA5 water, #1E1C18 ink
MOTION     contours reveal by elevation band as the reader scrolls, lowest first, so terrain fills from the valleys up
TELL       index contours are heavier and carry their elevation broken into the line itself, with the stroke stopping either side of the number

---

## Textile and fashion

### 25. Fabric swatch book
SOURCE     a Kvadrat or Maharam sample card: bound fabric chips, each with a specification block
SURFACE    real woven chips stapled to card, edges slightly frayed, the weave catching light differently at each angle
STRUCTURE  chips bound at one edge and fanned, each carrying a name, a code, composition, weight in grams per square metre, a Martindale rub count and a lightfastness rating
TYPE       `Karla` (names) + `Martian Mono` (codes and specifications)
COLOR      #E7E1D5 card, #3A4B3F moss, #8C3B2E rust, #2B3A55 indigo, #1A1917 print
MOTION     dragging spreads the stack along an arc; releasing lets it settle back with a short overshoot
TELL       each chip carries a real woven texture as a repeating canvas pattern, and no two chips share a texture even when they share a colour

### 26. Tailor's tissue pattern
SOURCE     a commercial dressmaking pattern: printed tissue pieces with notches, grainlines and cutting layouts
SURFACE    translucent tissue folded small, so creases cross every piece, with print showing through from the layer beneath
STRUCTURE  numbered pieces nested to save fabric, each with a grainline arrow, notches on the seam allowance, and a nested outline per size
TYPE       `Work Sans` (piece names) + `Cousine` (measurements and piece numbers)
COLOR      #F4F1E8 tissue, #2D2B26 print, #B0A896 shadow line, #C0392B cut line, #2E7D8F fold line
MOTION     dragging a piece shows its outline against the others and reports the fabric it saves
TELL       pieces are nested against a real fabric width and the leftover is visible, so the layout is an argument about waste rather than an arrangement

### 27. Jacquard punch card chain
SOURCE     a Jacquard loom card chain: stiff cards laced in a loop, each row of holes one pick of the weave
SURFACE    hard varnished card, cleanly punched holes, lacing cord through the edge holes, edges polished by the loom
STRUCTURE  a fixed grid of hole positions where presence or absence is the entire information content, cards sequential and looped so the pattern repeats exactly
TYPE       `Silkscreen` (card numbers) + `Libre Franklin` (labels)
COLOR      #C8B58E card, #2A2520 hole shadow, #6E5A3C lacing, #F0EAD8 highlight
MOTION     the chain advances one card per pick in discrete steps, and the weave grows one row at a time below it
TELL       the weave below is genuinely generated from the hole grid above, so changing a hole changes the cloth, and the loop repeats at the exact card count

### 28. Woven care label
SOURCE     the care label inside a garment: fibre content, origin, and the five ISO care symbols
SURFACE    woven polyester tape, letters formed from the weave so their edges are stepped, folded and stitched at both ends
STRUCTURE  fibre content, then origin, then care symbols in the fixed international order (wash, bleach, dry, iron, professional care), then the supplier code
TYPE       `Archivo Narrow` (all caps, tight) + `Space Mono` (codes)
COLOR      #F2F0EA tape, #1D1C19 weave black, #B33A2B red thread, #2E5E8C blue thread
MOTION     the label curls 6 degrees at its stitched end on hover and settles back
TELL       letterforms are rendered with a stepped low-resolution edge via a pixel grid or canvas threshold, because woven type cannot make a smooth curve

---

## Architecture and signage

### 29. Autobahn signage
SOURCE     German motorway signs: white on blue, DIN 1451 Mittelschrift, a fixed arrow and chevron system
SURFACE    retroreflective sheeting on aluminium, seen at speed, with a slight sheen and a rounded 20 mm border
STRUCTURE  destinations stacked by exit order each with a lane arrow, distances right aligned, sign size derived from content and reading distance rather than chosen
TYPE       `Chivo` (destinations) + `Saira Condensed` (distances and route numbers)
COLOR      #0057B8 motorway blue, #FFFFFF white, #F2C200 Bundesstrasse yellow, #1B1B1B border, #009B48 green
MOTION     sections scale from 0.94 to 1.0 on entry at a constant rate, never eased in
TELL       border radius, stroke weight and interior padding all derive from one cap-height unit, and every panel on the page obeys the same derivation

### 30. Munich 1972 identity system
SOURCE     Otl Aicher's identity for the 1972 Olympics: a pictogram grid and a banded colour system
SURFACE    flat printed panels and banners, no texture, no gradient, colour used at full area rather than as an accent
STRUCTURE  pictograms built strictly on a 0, 45 and 90 degree grid at one stroke weight, information banded into horizontal colour fields over a rigid module
TYPE       `Hanken Grotesk` (Univers lineage) + `Archivo Narrow` (numerals)
COLOR      #0F9D58 green, #4FB3D9 light blue, #7BC043 lime, #F5A623 orange, #F2F2F0 white
MOTION     colour bands wipe horizontally at 300ms on a section change. Pictograms never animate
TELL       every icon on the page is drawn on that same grid at that one stroke weight, which makes a stock icon set impossible to smuggle in

### 31. Paris enamel street plaque
SOURCE     the vitreous enamel street plaque of Paris: white letters on green inside a chamfered blue border
SURFACE    enamel fired onto steel, glassy specular highlight, one corner chipped to the steel, mounted on stone
STRUCTURE  arrondissement number in the top band, street type and name below in two weights, all inside a double border with rounded inner corners
TYPE       `Marcellus` (street name) + `Libre Franklin` (arrondissement and small text)
COLOR      #1F5C3D enamel green, #F4F2EC white, #1A3A6B border blue, #8E8577 stone, #B8B2A4 chip
MOTION     the specular highlight tracks the pointer slowly across the enamel and returns to rest when the pointer leaves
TELL       a real chamfer built from two nested borders and an inner shadow, with one corner chipped to expose the substrate colour

### 32. Board-formed concrete and terrazzo
SOURCE     a board-formed concrete wall over a terrazzo floor, as built in civic architecture of the 1960s
SURFACE    concrete carrying the grain and joint lines of the timber forms, tie holes at regular spacing, terrazzo with visible aggregate chips
STRUCTURE  horizontal board courses of constant height set the entire vertical rhythm, openings align to a course, and the terrazzo divider strips carry the plan grid
TYPE       `Familjen Grotesk` (headings) + `Space Mono` (labels and references)
COLOR      #B7B3AA concrete, #8E8A80 shadow, #E4E0D6 terrazzo, #3C3A34 aggregate, #A8452C brass divider
MOTION     a slow directional gradient rakes across the surface over 20 seconds, changing which courses catch light
TELL       tie holes appear at a real constant spacing derived from the course height, and every section boundary lands on a course line

---

## Screen and broadcast history

### 33. Ceefax teletext
SOURCE     BBC Ceefax, 1974: a 40 by 24 character grid, seven colours, graphics built from 2 by 3 block sixels
SURFACE    a CRT, phosphor bloom around bright characters, slight barrel distortion at the corners, scanline gaps
STRUCTURE  an absolute 40 by 24 character grid, a page number top left, a rolling index, and pictures assembled from block characters because nothing else exists
TYPE       `VT323` (body) + `DotGothic16` (headings and block graphics)
COLOR      #000000 ground, #FFFFFF white, #FFFF00 yellow, #00FFFF cyan, #00FF00 green
MOTION     pages load one row at a time from the top, and the corner page number cycles until the page arrives
TELL       every element lands exactly on the character cell grid, including images, which are built from block characters rather than being images

### 34. Test Card F
SOURCE     the BBC test card: geometry, greyscale and colour bars broadcast when there was nothing to broadcast
SURFACE    a still CRT image, a photographic centre inside a hard-edged geometric frame, held perfectly motionless
STRUCTURE  a centred circle inside a rectangle of castellations, a greyscale step wedge along the bottom, frequency gratings and colour bars at the sides, every element placed to test something specific
TYPE       `Barlow Condensed` (labels) + `VT323` (identifiers)
COLOR      #1A1A1A black level, #C8C8C8 white level, #0B7B8C cyan bar, #B8B300 yellow bar, #A31D2E red bar
MOTION     the card holds still. One element only, a hand or a sweeping bar, moves at exactly one step per second
TELL       the greyscale wedge is a real measured step wedge with its step values printed, and every geometric element states what it is testing

### 35. VHS J-card and tape label
SOURCE     a rental VHS: a printed J-card in the sleeve and a hand-written spine label on the cassette
SURFACE    glossy printed card gone soft at the folds, a matte adhesive label with ballpoint over its printed lines, a rewind sticker
STRUCTURE  artwork on the front, title running vertically on the spine, synopsis, running time, certificate and barcode in fixed positions on the back
TYPE       `Archivo Black` (title) + `Caveat` (the handwritten spine label)
COLOR      #17161A card black, #E8E3D6 label, #D8232A certificate red, #F2B705 rental yellow, #2F6FA8 blue
MOTION     hovering a title slides the cassette 12 px out of its sleeve. Nothing else moves
TELL       running time, certificate and catalogue number exist on every item in the same corner in printed type, and only the spine label is handwritten

---

## Craft and workshop

### 36. Hi-fi service manual
SOURCE     a Japanese hi-fi service manual: block diagrams, schematics, printed circuit layouts and a parts list
SURFACE    thin manual paper, two-colour print, folded schematic sheets bound in and larger than the page
STRUCTURE  block diagram, then schematic, then board layout, then a parts table of reference designator, description, part number and note, with alignment procedures citing designators
TYPE       `IBM Plex Sans Condensed` (headings and procedures) + `IBM Plex Mono` (parts list and designators)
COLOR      #F1EDE1 paper, #1A1A17 ink, #B0341F second colour, #6E6A5C rule, #C9C3B0 fold shadow
MOTION     selecting a stage brightens its signal path through the block diagram from input to output in one pass
TELL       every component on the diagram carries a reference designator that resolves to a parts-list row, and the resolution works in both directions

### 37. Darkroom contact sheet
SOURCE     a photographer's contact sheet with grease pencil selects and crop marks
SURFACE    glossy fibre paper, frames printed edge to edge with the film rebate showing, wax pencil sitting on top of the emulsion
STRUCTURE  frames in strict rows in shooting order, frame numbers in the rebate, selects circled, rejects crossed, crops drawn as corner marks, a note in the white margin
TYPE       `Cousine` (frame numbers and notes) + `Permanent Marker` (the pencil marks)
COLOR      #14140F paper black, #E7E2D4 rebate, #E8452F grease red, #F2C200 grease yellow, #8E8A7C margin
MOTION     circles and crosses stroke on in a single 220ms pass, in the order they were originally made
TELL       the film rebate with frame numbers sits between frames, and the grease marks sit above the image on a multiply blend so the image reads through them

### 38. Hardware store bin labels
SOURCE     the bin fronts of an old ironmonger: a part code, a name, a count, a unit price and a price per hundred
SURFACE    painted steel bins, a card label in a metal clip, the count written in pencil and rubbed out several times
STRUCTURE  a wall of bins in a rigid grid where the grid is the navigation, each label carrying code, name, unit price, price per hundred and a hand-written count
TYPE       `Anton` (bin codes) + `Courier Prime` (names and prices)
COLOR      #3E4A3F bin green, #E4DFCE label card, #1B1A16 ink, #A8321F price red, #9AA39B steel
MOTION     selecting a bin slides its front forward 8 px with a hard stop, and the count updates in place
TELL       every bin shows its real count including zero, and a zero bin stays in the grid with its label instead of disappearing

### 39. Letterpress composing stick and chase
SOURCE     hand composition: type set in a stick, locked into a chase with wooden furniture and iron quoins
SURFACE    lead type face-up under raking light, wooden furniture, iron quoins, ink on the face where the forme was proofed
STRUCTURE  the measure is fixed by the stick so every line is justified with real spacing material, and blocks are locked in place by furniture, which is visible as the negative space
TYPE       `Sorts Mill Goudy` (text) + `Archivo Narrow` (folios and marginalia)
COLOR      #E9E3D3 stock, #1B1915 ink, #7B7266 lead, #8A6A3F furniture, #4A4F52 quoin iron
MOTION     on load, blocks slide the last few pixels into their locked position and stop hard, once
TELL       every gap on the page is a rectangle drawn from a fixed set of furniture sizes, so no margin is ever an arbitrary value

### 40. Blue Note record sleeve
SOURCE     a Blue Note LP sleeve art directed by Reid Miles over a Francis Wolff session photograph
SURFACE    printed board with ring wear at the disc edge, a duotone photograph, two spot colours and the paper
STRUCTURE  the photograph takes a cropped block and the type does everything else: an enormous tightly tracked title, personnel small in a corner, colour laid as flat fields rather than accents
TYPE       `Libre Franklin` (personnel and body) + `Archivo Black` (title, tracked tight)
COLOR      #E9E3D2 board, #14130F black, #D8471F orange, #1F6FA8 blue, #F2C200 yellow
MOTION     the sleeve rotates 3 degrees on hover and the ring wear catches light. The record itself never spins
TELL       the personnel list is complete with instruments and set at a size that respects the format, never scaled to fill a gap

---

## HOW TO ASSIGN

### Step 1. Draw by an external index, never by preference

The agent does not pick. It computes an index from something outside its own ranking: the project
slug, the date, or a number the user supplies. Same inputs, same worlds, and no run can quietly
converge on a favourite.

```js
// draw.mjs <slug> [salt]   salt defaults to today, so the same project can be re-rolled by date
const slug = process.argv[2];
const salt = process.argv[3] ?? new Date().toISOString().slice(0, 10);
let h = 2166136261;
for (const ch of `${slug}:${salt}`) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); }
const a = (h >>> 0) % 40 + 1;
const raw = (Math.imul((h >>> 0) ^ 0x9e3779b9, 2654435761) >>> 0) % 39 + 1;
const b = raw >= a ? raw + 1 : raw;      // guarantees b !== a
console.log(`WORLD A ${a}  WORLD B ${b}  seed ${slug}:${salt}`);
```

Record the seed string in the direction contract's FORM block. A direction whose seed is not written
down cannot be audited and cannot be reproduced.

If no script is available, the fallback index is the sum of the character codes of the project slug
modulo 40, plus one. Announce which method was used.

### Step 2. Exclude the rut, then exclude its opposite

Before the draw, write down two things from the vertical playbook:

1. **The rut.** What every site in this category already ships, described concretely enough that a
   world can be tested against it.
2. **The obvious contrarian.** What the category produces the moment it is told to be different.
   Predictable contrarianism is also a prior.

Then apply the exclusions:

- If a drawn world would render as the rut, it is excluded. Take the next index, do not choose a replacement.
- If a drawn world would render as the obvious contrarian, it is excluded the same way.
- A world is not excluded because it feels risky. Taste is never grounds for a re-draw. Only a
  factual conflict is: the world cannot carry the product's truth, the assets do not exist, or the
  performance budget cannot pay for it.
- **The test:** if someone could guess the aesthetic from the category alone, or from
  category-plus-avoidance, the exclusion has not bitten yet. Draw again.

Each drawn world must pass a viability gate before it is used: every relationship it visualises is
true, the palette and component family are real, the assets exist or can be authored, and it works at
full-surface scale inside the performance budget. A world that fails on truth is replaced before the
draw, never rescued after it.

### Step 3. Fuse two worlds, judge on exactly two axes

The draw returns two indices. The fusion is the direction.

- **World A supplies the form and its system grammar:** structure, topology, controls, states, motion,
  responsive behaviour. It is a working system, not a mood reference.
- **World B supplies one dominant material or mechanism:** its surface, its colour logic, or its TELL.
  Not its whole structure. Two structures fused is mush.
- **The product supplies every fact.** Clarity wins every conflict between the fusion and the content.

Judge the fused result on exactly two axes and nothing else:

| Axis | Question |
|---|---|
| **Audience identification** | Does the audience for this product recognise this world and read it as theirs? |
| **Product clarity** | Is the product's actual mechanism clearer inside this world than outside it? |

Two axes, not five. A longer rubric is how the safe option wins on points.

Losing to strong grounded material is a valid outcome. Beating a thin list is the point.

### Step 4. The standing exit

The category standard, played straight, is always available to the user. Never recommend it, never
weigh it against the draw, never let it soften a dealt direction. If the user takes it, ask once for
two or three products this should sit beside, make their craft level the bar, and execute the
convention at full fidelity with no irony and no smuggled quirk.

### Step 5. Commit

Carry the surviving world's working system into the product: palette and material, type and
composition, topology, controls and state, responsive rules. Rebuild nav, buttons, inputs and links
in the world's own vocabulary. A stock component inside a committed form is a lapse.

A rendition that matches what any model already ships for that world failed at execution, not at
selection. The world was pinned, not its softest reading.
