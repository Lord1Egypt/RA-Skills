#!/usr/bin/env python3
"""
pptxgenjs PPTX Compatibility Fixer

Fixes known pptxgenjs defects that trigger PowerPoint's "problem with content" repair dialog.
Based on: https://github.com/gitbrent/PptxGenJS/issues/1449

Usage:
    python fix_pptx_compatibility.py <input.pptx> [output.pptx]

If output is omitted, overwrites the input file.
"""

import sys
import os
import re
import zipfile
import tempfile
import shutil
import xml.etree.ElementTree as ET


def fix_content_types_xml(content_bytes, existing_files):
    """Fix [Content_Types].xml — the #1 cause of repair dialog.
    
    pptxgenjs generates phantom slideMaster Override entries for every slide,
    but only slideMaster1.xml actually exists. These phantom references trigger
    PowerPoint's repair dialog.
    
    Also removes unused Default extension types that bloat the file.
    """
    # Register namespaces to preserve them on write
    ET.register_namespace('', 'http://schemas.openxmlformats.org/package/2006/content-types')
    
    root = ET.fromstring(content_bytes)
    ns = {'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}
    
    removed_overrides = 0
    removed_defaults = 0
    
    # Fix phantom slideMaster overrides — keep only those whose PartName points to an existing file
    overrides_to_remove = []
    for override in root.findall('ct:Override', ns):
        part_name = override.get('PartName', '')
        if part_name.startswith('/'):
            relative_path = part_name[1:]
        else:
            relative_path = part_name
        
        if 'slideMaster' in part_name and relative_path not in existing_files:
            overrides_to_remove.append(override)
    
    for override in overrides_to_remove:
        root.remove(override)
        removed_overrides += 1
    
    # Remove unused Default extension types (jpeg, jpg, svg, gif, m4v, mp4, vml, xlsx)
    # Only keep: rels, xml, png (commonly used)
    safe_defaults = {'rels', 'xml', 'png'}
    defaults_to_remove = []
    for default in root.findall('ct:Default', ns):
        ext = default.get('Extension', '')
        if ext not in safe_defaults:
            # Check if any file with this extension exists
            has_files = any(
                f'.{ext}' in fname for fname in existing_files
            )
            if not has_files:
                defaults_to_remove.append(default)
    
    for default in defaults_to_remove:
        root.remove(default)
        removed_defaults += 1
    
    fixed_bytes = ET.tostring(root, encoding='unicode', xml_declaration=True)
    # Ensure proper XML declaration
    if not fixed_bytes.startswith('<?xml'):
        fixed_bytes = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + fixed_bytes
    
    return fixed_bytes.encode('utf-8'), removed_overrides, removed_defaults


def fix_slide_xml(content_bytes, filename):
    """Fix individual slide XML files with known pptxgenjs defects."""
    content = content_bytes.decode('utf-8')
    fixes = 0
    
    # Fix 1: Invalid theme font references (+mn-lt, +mn-ea, +mn-cs, +mj-lt, +mj-ea, +mj-cs)
    # Replace with Microsoft YaHei (safe cross-platform CJK font)
    invalid_fonts = ['+mn-lt', '+mn-ea', '+mn-cs', '+mj-lt', '+mj-ea', '+mj-cs']
    for font in invalid_fonts:
        if font in content:
            content = content.replace(font, 'Microsoft YaHei')
            fixes += 1
    
    # Fix 2: Remove dirty= attribute (non-standard pptxgenjs attribute)
    dirty_pattern = re.compile(r'\s+dirty="[^"]*"')
    dirty_matches = dirty_pattern.findall(content)
    if dirty_matches:
        content = dirty_pattern.sub('', content)
        fixes += len(dirty_matches)
    
    # Fix 3: Remove p14:modId elements (non-standard namespace, triggers repair)
    modid_pattern = re.compile(r'<p14:modId[^>]*/?\s*>', re.DOTALL)
    modid_matches = modid_pattern.findall(content)
    if modid_matches:
        content = modid_pattern.sub('', content)
        fixes += len(modid_matches)
    # Also handle multi-line modId
    modid_pattern2 = re.compile(r'<p14:modId[^>]*>.*?</p14:modId>', re.DOTALL)
    modid_matches2 = modid_pattern2.findall(content)
    if modid_matches2:
        content = modid_pattern2.sub('', content)
        fixes += len(modid_matches2)
    
    # Fix 4: Zero-extent shapes (cx="0" cy="0") — replace with minimum 1 EMU
    zero_ext_pattern = re.compile(r'cx="0"')
    zero_matches = zero_ext_pattern.findall(content)
    if zero_matches:
        content = zero_ext_pattern.sub('cx="1"', content)
        fixes += len(zero_matches)
    
    zero_ext_pattern2 = re.compile(r'cy="0"')
    zero_matches2 = zero_ext_pattern2.findall(content)
    if zero_matches2:
        content = zero_ext_pattern2.sub('cy="1"', content)
        fixes += len(zero_matches2)
    
    # Fix 5: Empty text elements <a:t></a:t> — replace with space
    empty_text_pattern = re.compile(r'<a:t></a:t>')
    empty_matches = empty_text_pattern.findall(content)
    if empty_matches:
        content = empty_text_pattern.sub('<a:t> </a:t>', content)
        fixes += len(empty_matches)
    
    # Fix 6: Empty line elements <a:ln /> — replace with proper noFill
    empty_ln_pattern = re.compile(r'<a:ln\s*/>')
    empty_ln_matches = empty_ln_pattern.findall(content)
    if empty_ln_matches:
        content = empty_ln_pattern.sub('<a:ln w="0"><a:noFill/></a:ln>', content)
        fixes += len(empty_ln_matches)
    
    return content.encode('utf-8'), fixes


def fix_rels_xml(content_bytes, filename):
    """Remove relationships pointing to non-existent files (notesSlides, notesMasters)."""
    content = content_bytes.decode('utf-8')
    fixes = 0
    
    # Remove notesSlides and notesMasters relationships (pptxgenjs generates broken ones)
    ns_pattern = re.compile(r'<Relationship[^>]*Target="[^"]*notesSlide[^"]*"[^>]*/>')
    ns_matches = ns_pattern.findall(content)
    if ns_matches:
        content = ns_pattern.sub('', content)
        fixes += len(ns_matches)
    
    nm_pattern = re.compile(r'<Relationship[^>]*Target="[^"]*notesMaster[^"]*"[^>]*/>')
    nm_matches = nm_pattern.findall(content)
    if nm_matches:
        content = nm_pattern.sub('', content)
        fixes += len(nm_matches)
    
    return content.encode('utf-8'), fixes


def fix_pptx(input_path, output_path=None):
    """Main fix function — processes all known pptxgenjs compatibility issues."""
    if output_path is None:
        output_path = input_path
    
    print(f"🔍 Analyzing: {input_path}")
    
    with zipfile.ZipFile(input_path, 'r') as z:
        file_list = z.namelist()
        existing_files = set(file_list)
        
        # Identify files to process
        content_types_data = z.read('[Content_Types].xml')
        slide_files = [f for f in file_list if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
        rels_files = [f for f in file_list if f.endswith('.rels') and 'ppt/' in f]
        
        # Files to exclude from output (notesSlides and notesMasters)
        exclude_files = [f for f in file_list if 'notesSlide' in f or 'notesMaster' in f]
        
        # Fix Content_Types.xml
        ct_fixed, removed_overrides, removed_defaults = fix_content_types_xml(content_types_data, existing_files)
        print(f"  ✅ [Content_Types].xml: removed {removed_overrides} phantom overrides, {removed_defaults} unused defaults")
        
        # Fix slide XMLs
        total_slide_fixes = 0
        slide_contents = {}
        for sf in slide_files:
            data = z.read(sf)
            fixed, count = fix_slide_xml(data, sf)
            slide_contents[sf] = fixed
            total_slide_fixes += count
        
        print(f"  ✅ Slides: {total_slide_fixes} fixes across {len(slide_files)} slides")
        
        # Fix rels files
        total_rels_fixes = 0
        rels_contents = {}
        for rf in rels_files:
            data = z.read(rf)
            fixed, count = fix_rels_xml(data, rf)
            rels_contents[rf] = fixed
            total_rels_fixes += count
        
        print(f"  ✅ Relationships: {total_rels_fixes} broken refs removed")
        
        if exclude_files:
            print(f"  ✅ Excluding {len(exclude_files)} notes files")
        
        # Write fixed PPTX
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as out:
            for item in file_list:
                # Skip excluded files
                if item in exclude_files:
                    continue
                
                if item == '[Content_Types].xml':
                    out.writestr(item, ct_fixed)
                elif item in slide_contents:
                    out.writestr(item, slide_contents[item])
                elif item in rels_contents:
                    out.writestr(item, rels_contents[item])
                else:
                    out.writestr(item, z.read(item))
    
    size_kb = os.path.getsize(output_path) / 1024
    print(f"\n✅ Fixed PPTX saved: {output_path} ({size_kb:.1f} KB)")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_pptx_compatibility.py <input.pptx> [output.pptx]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    fix_pptx(input_file, output_file)
