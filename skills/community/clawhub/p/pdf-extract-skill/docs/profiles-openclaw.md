# OpenClaw Profiles (Ready Commands)

## Profile 1: Fast reading
opendataloader-pdf ./pdfs/ -o ./output -f markdown

## Profile 2: Recommended for RAG
opendataloader-pdf ./pdfs/ -o ./output -f json,markdown

## Profile 3: Specific pages only
opendataloader-pdf report.pdf -o ./output -f json --pages "1,3,5-7"

## Profile 4: Sanitize sensitive data
opendataloader-pdf report.pdf -o ./output -f markdown --sanitize

## Profile 5: Keep line breaks
opendataloader-pdf report.pdf -o ./output -f markdown --keep-line-breaks

## Profile 6: External images
opendataloader-pdf report.pdf -o ./output -f json --image-output external

## Profile 7: Embedded images
opendataloader-pdf report.pdf -o ./output -f json --image-output embedded
