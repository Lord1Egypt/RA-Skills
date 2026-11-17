const EMPL_TPL={dlg:false,name:'',tpl:'',cmt:'',isEdit:false};
export default {
inject:['service', 'tags'],
data() {return {
    tmpls:[],
    tmplInfo:cloneObj(EMPL_TPL)
}},
created(){
    this.getTmpls();
},
methods:{
getTmpls() {
    this.service.getTmpls(true).then(tmpls => {
        this.tmpls=tmpls;
    });
},
setTmpl() {
    var dta=copyObj(this.tmplInfo,['name','cmt','tpl']);
    var url;
    var method;
    if(this.tmplInfo.isEdit) {
        url = "/api/msgtpl/update";
        method="PUT";
    } else {
        url = "/api/msgtpl/add";
        method="POST";
    }
    request({method:method,url:url,data:dta}, this.service.name).then(resp => {
        if(resp.code != 0) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        this.getTmpls();
        this.tmplInfo.dlg=false;
    })
},
rmvTmpl() {
    var url="/api/msgtpl/remove?name="+encodeURIComponent(this.tmplInfo.name);
    request({method:"DELETE",url:url}, this.service.name).then(resp => {
        if(resp.code != 0) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        this.getTmpls();
        this.tmplInfo.dlg=false;
    })
},
showEdit(i) {
    var t;
    if(i>=0) {
        t=cloneObj(this.tmpls[i]);
        t.title=this.tags.editTmpl;
        t.isEdit=true;
    } else {
        t=cloneObj(EMPL_TPL);
        t.title=this.tags.addTmpl;
        t.isEdit=false;
    }
    t.dlg=true;
    this.tmplInfo=cloneObj(t);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.go_back"></q-btn>
    <q-toolbar-title>{{tags.homeMenus.tpl.name}}</q-toolbar-title>
    <q-btn flat dense icon="playlist_add" @click="showEdit(-1)" color="white"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<q-list separator>
<q-item v-for="(t,i) in tmpls" clickable @click="showEdit(i)">
 <q-item-section>
    <q-item-label>{{t.name}}</q-item-label>
    <q-item-label caption>{{t.cmt}}</q-item-label>
 </q-item-section>
 <q-item-section style="line-break: anywhere;">{{t.tpl}}</q-item-section>
</q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" :close="tags.close" ref="errDlg"></component-alert-dialog>

<!-- 增加/修改模板弹窗 -->
<q-dialog v-model="tmplInfo.dlg" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
     <div class="text-h6">{{tmplInfo.title}} {{tmplInfo.name}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
        <q-input v-model="tmplInfo.name" :label="tags.tmpl.name" maxlength=30 dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
        <q-input v-model="tmplInfo.tpl" :label="tags.tmpl.tpl"  maxlength=300 dense></q-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="tmplInfo.cmt" :label="tags.tmpl.cmt" dense maxlength=300 type="textarea"></q-input>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click.stop="setTmpl"></q-btn>
      <q-btn v-show="tmplInfo.isEdit" flat :label="tags.remove" color="red" @click.stop="rmvTmpl"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>
`
}