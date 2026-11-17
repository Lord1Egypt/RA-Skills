param([Parameter(Mandatory=$true)][string]$InputDoc,[Parameter(Mandatory=$true)][string]$OutputDocx)
$source=(Resolve-Path -LiteralPath $InputDoc).Path; $target=[IO.Path]::GetFullPath($OutputDocx)
if([IO.Path]::GetExtension($source).ToLowerInvariant() -ne '.doc'){throw '输入必须是 .doc 文件。'}
if([IO.Path]::GetExtension($target).ToLowerInvariant() -ne '.docx'){throw '输出必须是 .docx 文件。'}
$app=$null; $document=$null; $provider=$null
foreach($candidate in @('Word.Application','kwps.Application')){try{$app=New-Object -ComObject $candidate;$provider=$candidate;break}catch{$app=$null}}
if($null -eq $app){throw '未找到可自动化的 Microsoft Word 或 WPS，无法可靠地将 .doc 转换为 .docx。'}
try{$app.Visible=$false;$document=$app.Documents.Open($source);try{$document.SaveAs2($target,16)}catch{$document.SaveAs($target,12)};[pscustomobject]@{Provider=$provider;Input=$source;Output=$target}}
finally{if($null -ne $document){$document.Close($false)};if($null -ne $app){$app.Quit()}}
