# JSON actions

Actions inspect(template), render(template,data:{field:value}) or render(template,rows:[{outputName,data:{...}}],outputDirectory optional). Template workspace-relative DOCX/TXT/MD/HTML/CSV <=20MiB (expanded DOCX<=100MiB). Placeholder keys [A-Za-z_][A-Za-z0-9_.-]*. OutputName portable identifier; suffix follows source. Outputs default exports/documents; 1..200 records; missing fields or output-name conflicts stop before rendering. Existing output files are preserved. Sample template at samples/template.txt.
