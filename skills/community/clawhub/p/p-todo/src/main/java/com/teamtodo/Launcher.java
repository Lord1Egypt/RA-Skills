package com.teamtodo;

/**
 * 启动包装类：在 JPMS 环境下，JavaFX 的 main 需要放在非导出模块根，
 * 或由此类作为非模块入口调用。
 */
public class Launcher {
    public static void main(String[] args) {
        App.main(args);
    }
}
