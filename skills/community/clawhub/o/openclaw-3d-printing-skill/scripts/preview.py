#!/usr/bin/env python3
"""Render a simple CadQuery STL preview using pyrender."""

from __future__ import annotations

import argparse
import math
import os
import platform

import numpy as np

if platform.system() == "Linux" and "PYOPENGL_PLATFORM" not in os.environ:
    os.environ["PYOPENGL_PLATFORM"] = "egl"

import pyrender
import trimesh
from PIL import Image, ImageDraw, ImageFont

from mesh_io import load_mesh


def camera_pose(elev_deg: float, azim_deg: float, distance: float, center: np.ndarray) -> np.ndarray:
    elev = math.radians(elev_deg)
    azim = math.radians(azim_deg)
    eye = np.array([
        math.cos(elev) * math.cos(azim),
        math.cos(elev) * math.sin(azim),
        math.sin(elev),
    ]) * distance + center

    forward = center - eye
    forward = forward / np.linalg.norm(forward)
    up = np.array([0.0, 0.0, 1.0])
    right = np.cross(forward, up)
    if np.linalg.norm(right) < 1e-6:
        up = np.array([0.0, 1.0, 0.0])
        right = np.cross(forward, up)
    right = right / np.linalg.norm(right)
    up = np.cross(right, forward)

    pose = np.eye(4)
    pose[:3, 0] = right
    pose[:3, 1] = up
    pose[:3, 2] = -forward
    pose[:3, 3] = eye
    return pose


def build_scene(mesh: trimesh.Trimesh) -> tuple[pyrender.Scene, float, np.ndarray]:
    mesh.fix_normals()
    material = pyrender.MetallicRoughnessMaterial(
        baseColorFactor=[0.35, 0.58, 0.9, 1.0],
        metallicFactor=0.05,
        roughnessFactor=0.65,
        doubleSided=True,
    )
    scene = pyrender.Scene(bg_color=[0.95, 0.95, 0.97, 1.0], ambient_light=[0.35, 0.35, 0.35])
    scene.add(pyrender.Mesh.from_trimesh(mesh, smooth=True, material=material))

    for direction in ([1, 1, 1], [-1, 1, 1], [0, -1, 1]):
        light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=2.5)
        direction = np.array(direction, dtype=float)
        direction /= np.linalg.norm(direction)
        pose = np.eye(4)
        pose[:3, 2] = -direction
        scene.add(light, pose=pose)

    center = mesh.bounding_box.centroid
    radius = float(np.linalg.norm(mesh.bounding_box.extents) / 2.0) or 1.0
    return scene, radius, center


def render_frame(scene: pyrender.Scene, radius: float, center: np.ndarray, elev: float, azim: float, width: int, height: int) -> Image.Image:
    cam = pyrender.PerspectiveCamera(yfov=math.radians(35))
    pose = camera_pose(elev, azim, radius * 3.2, center)
    cam_node = scene.add(cam, pose=pose)
    renderer = pyrender.OffscreenRenderer(width, height)
    try:
        color, _ = renderer.render(scene)
    finally:
        renderer.delete()
        scene.remove_node(cam_node)
    return Image.fromarray(color)


def annotate(image: Image.Image, mesh: trimesh.Trimesh, label: str) -> Image.Image:
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    bb = mesh.bounding_box.extents
    footer = f"{label} | {bb[0]:.1f} x {bb[1]:.1f} x {bb[2]:.1f} mm | {'watertight' if mesh.is_watertight else 'not watertight'}"
    draw.rectangle((0, image.height - 18, image.width, image.height), fill=(245, 245, 245))
    draw.text((8, image.height - 15), footer, fill=(0, 0, 0), font=font)
    return image


def render(mesh: trimesh.Trimesh, output_path: str, views: str = "multi") -> str:
    scene, radius, center = build_scene(mesh)
    if views == "iso":
        image = render_frame(scene, radius, center, 28, 35, 900, 700)
        annotate(image, mesh, "isometric").save(output_path)
        return output_path

    presets = [
        (28, 35, "iso"),
        (0, 0, "front"),
        (90, 0, "top"),
        (0, 90, "right"),
    ]
    frames = [annotate(render_frame(scene, radius, center, elev, azim, 500, 420), mesh, label) for elev, azim, label in presets]
    sheet = Image.new("RGB", (1000, 840), (250, 250, 252))
    positions = [(0, 0), (500, 0), (0, 420), (500, 420)]
    for frame, position in zip(frames, positions):
        sheet.paste(frame, position)
    sheet.save(output_path)
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render STL previews")
    parser.add_argument("stl_path")
    parser.add_argument("output_path")
    parser.add_argument("--views", choices=["iso", "multi"], default="multi")
    args = parser.parse_args()

    mesh = load_mesh(args.stl_path)
    render(mesh, args.output_path, args.views)
    print(args.output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
