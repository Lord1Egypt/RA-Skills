module com.teamtodo {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.swing;
    requires javafx.graphics;
    requires java.sql;
    requires java.prefs;
    requires java.desktop;  // 系统托盘
    requires jdk.httpserver; // REST API 服务器
    requires com.zaxxer.hikari;
    requires com.google.gson;
    requires org.slf4j;

    opens com.teamtodo to javafx.fxml;
    opens com.teamtodo.controller to javafx.fxml;
    opens com.teamtodo.model to com.google.gson;
    opens com.teamtodo.model.enums to com.google.gson;

    exports com.teamtodo;
    exports com.teamtodo.controller;
    exports com.teamtodo.model;
    exports com.teamtodo.model.enums;
    exports com.teamtodo.service;
    exports com.teamtodo.util;
}
